from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, RatingSerializer
from .models import Movie, Actor, Rating
from categories.models import Category
import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.exceptions import ValidationError

User = get_user_model()

TMDB_API_KEY = settings.API_KEY
# Create your views here.
# 영화 상세 정보 조회
# @api_view(['GET'])
# def movie_detail(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     serializer = MovieSerializer(movie)
#     return JsonResponse(serializer.data)

# 영화 검색

def search_movie(request):
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)

    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ko-KR&include_adult=false'
    response = requests.get(url)
    data = response.json()
    results = []
    for movie in data.get('results', []):
        results.append({
            'id': movie['id'],
            'title': movie['title'],
            'poster': movie['poster_path'],
            'ranking': movie['vote_average'],
            # 'runtime': movie['runtime'],
        })

    return JsonResponse({'results': results})



# 영화 상세 정보 조회
@api_view(['GET'])
def search_and_get_movie_detail(request, movie_id):
    try:
        # 내 데이터베이스에서 해당 영화를 조회합니다.
        movie = Movie.objects.filter(pk=movie_id).first()

        if movie:
            # 내 데이터베이스에 저장된 정보가 있다면 해당 정보를 사용하여 출력합니다.
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        else:
            # 내 데이터베이스에 저장된 정보가 없다면 TMDb API를 통해 영화의 상세 정보를 가져옵니다.
            url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits&language=ko-KR'
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                return Response({'error': 'Movie not found'}, status=404)

            # 가져온 정보를 내 데이터베이스에 저장합니다.
            genre_ids = [genre['id'] for genre in data.get('genres', [])]
            actor_data = []
            for actor in data.get('credits', {}).get('cast', []):
                if actor.get('known_for_department') == 'Acting':
                    actor_instance, _ = Actor.objects.get_or_create(
                        id=actor['id'],
                        defaults={'name': actor['original_name'], 'profile_url': actor['profile_path']}
                    )
                    actor_data.append(actor_instance)

            # 새로운 영화를 생성하고 배우를 설정합니다.
            new_movie = Movie.objects.create(
                id=movie_id,
                title=data.get('title'),
                content=data.get('overview'),
                release_date=data.get('release_date'),
                runtime=data.get('runtime'),
                rank=data.get('vote_average'),
                poster_path=data.get('poster_path'),
            )
            new_movie.genres.set(genre_ids)
            new_movie.actors.set(actor_data)

            # 생성된 영화 정보를 출력합니다.
            serializer = MovieSerializer(new_movie)
        return Response(serializer.data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# 영화 평점 등록
@api_view(['POST'])
def create_rating(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)
    rating = movie.ratings.filter(user=user).first()
    serializer = RatingSerializer(data=request.data)
    if not rating:
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            ratings = movie.ratings.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 이미 평점을 등록했다면 평점 수정해버리기 - 한 사람이 한 영화에 대해 여러 평점 x
    else:
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 평점 삭제
@api_view(['PUT', 'DELETE'])
def rating_update_or_delete(request, movie_pk, rating_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = get_object_or_404(Rating, pk=rating_pk)
    def get_movie_ratings(request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        ratings = movie.ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_rating():
        if request.user == rating.user:
            serializer = RatingSerializer(instance=rating, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                ratings = movie.ratings.all()
                serializer = RatingSerializer(ratings, many=True)
                return Response(serializer.data)

    def delete_rating():
        if request.user == rating.user:
            rating.delete()
            ratings = movie.ratings.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data)
    
    if request.method == 'PUT':
        return update_rating()
    elif request.method == 'DELETE':
        return delete_rating()
    elif request.method == 'GET':
        return get_movie_ratings(request, movie_pk)

##### 영화 추천 알고리즘

def get_movie_genres(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return ', '.join([genre['name'] for genre in genres])
    return ''

def get_all_movies():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=ko-KR&sort_by=popularity.desc&page=10"
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get('results', [])
        return [(movie['id'], movie['title'], f"https://image.tmdb.org/t/p/original{movie['poster_path']}") for movie in movies if movie['poster_path']]
    return []

@api_view(['GET'])
def recommend_movies(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)
    
    user_id = request.user.id
    category = Category.objects.filter(user_id=user_id, name='Category1').first()
    
    if not category:
        return Response({'error': 'Category not found'}, status=404)
    
    movie_ids = category.movies.values_list('id', flat=True)
    unique_genres = Movie.objects.filter(id__in=movie_ids).values_list('genres__name', flat=True).distinct()
    
    if not unique_genres:
        return Response({'error': 'No genres found for the movies in the category'}, status=404)
    
    selected_genres_str = ', '.join(unique_genres)

    # TMDB API를 통해 모든 영화와 장르 정보를 가져옵니다.
    all_movies = get_all_movies()
    movies_with_genres = [(movie_id, movie_title, poster_url, get_movie_genres(movie_id)) for movie_id, movie_title, poster_url in all_movies]

    # 데이터 프레임 생성
    df = pd.DataFrame(movies_with_genres, columns=['movie_id', 'title', 'poster_path', 'genres'])

    # pd.concat을 사용하여 Series를 연결합니다.
    vectorizer = CountVectorizer()
    genre_matrix = vectorizer.fit_transform(pd.concat([df['genres'], pd.Series([selected_genres_str])]))

    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(genre_matrix[-1], genre_matrix[:-1])

    # 유사도에 따라 영화들을 정렬하고 상위 N개를 선택
    N = 5
    recommended_movie_indices = cosine_sim.argsort()[0][-N:][::-1]
    recommended_movies = df.iloc[recommended_movie_indices]

    # 추천 영화 제목과 포스터 URL 반환
    recommended_movies_list = recommended_movies[['movie_id', 'title', 'poster_path']].to_dict(orient='records')

    return JsonResponse({'recommended_movies': recommended_movies_list})


##### 영화 추천 (일단 지우지 말아요)

# def fetch_genre_id_to_name_map():
#     url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US'
#     response = requests.get(url)
#     genre_id_to_name = {}
#     if response.status_code == 200:
#         genres = response.json()['genres']
#         for genre in genres:
#             genre_id_to_name[genre['id']] = genre['name']
#     else:
#         print(f'Error fetching genres from TMDB, status code: {response.status_code}')
#     return genre_id_to_name

# def fetch_popular_movies_from_tmdb():
#     try:
#         url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()['results']  # 인기 영화 목록 반환
#         else:
#             print(f'Error fetching data from TMDB, status code: {response.status_code}')
#             return None
#     except requests.RequestException as e:
#         print(f'Request to TMDB failed: {e}')
#         return None

# @api_view(['GET'])
# def recommend_movies(request):
#     if not request.user.is_authenticated:
#         return Response({'error': 'User not authenticated'}, status=401)
    
#     user_id = request.user.id
#     category = Category.objects.filter(user_id=user_id, name='Category1').first()
    
#     if not category:
#         return Response({'error': 'Category not found'}, status=404)
    
#     movie_ids = category.movies.values_list('id', flat=True)
#     unique_genres = Movie.objects.filter(id__in=movie_ids).values_list('genres__name', flat=True).distinct()
    
#     if not unique_genres:
#         return Response({'error': 'No genres found for the movies in the category'}, status=404)
    
#     genre_names = ' '.join(list(unique_genres))  # 장르 이름을 공백으로 구분된 문자열로 변환
#     tfidf_vectorizer = TfidfVectorizer(stop_words='english')
#     user_genre_tfidf = tfidf_vectorizer.fit_transform([genre_names])
    
#     popular_movies = fetch_popular_movies_from_tmdb()
#     if not popular_movies:
#         return Response({'error': 'Failed to fetch popular movies from TMDB'}, status=500)
    
#     genre_id_to_name_map = fetch_genre_id_to_name_map()  # 장르 ID와 이름 매핑

#     recommendations = []
#     for movie in popular_movies:
#         # TMDB API에서 장르 ID를 사용해 장르 이름 추출
#         movie_genres = ' '.join([genre_id_to_name_map[genre_id] for genre_id in movie['genre_ids'] if genre_id in genre_id_to_name_map])
        
#         movie_genre_tfidf = tfidf_vectorizer.transform([movie_genres])
        
#         # 유사도 계산
#         cosine_sim = cosine_similarity(user_genre_tfidf, movie_genre_tfidf)[0][0]
        
#         # 유사도가 높은 영화 추천 목록에 추가
#         if cosine_sim > 0.35:  # 유사도 임계값은 조정 가능합니다.
#             recommendations.append({
#                 'id': movie['id'],
#                 'title': movie['title'],
#                 'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
#                 'similarity_score': cosine_sim
#             })
        
#         # 유사도 점수 기준으로 내림차순 정렬
#         recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    
#     # 상위 5개 영화 추천
#     return Response(recommendations[:5])