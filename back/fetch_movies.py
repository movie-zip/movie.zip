import os
import django
import requests
import json

# Django 설정을 초기화합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from django.conf import settings

API_KEY = settings.API_KEY

def get_movie_datas():
    total_data = []
    actor_data = []

    # 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 101):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&page={i}"
        response = requests.get(request_url)
        if response.status_code != 200:
            print(f"Error fetching data from TMDb API: {response.status_code}")
            return

        movies = response.json()
        for movie in movies['results']:
            if movie.get('release_date', ''):
                details = get_movie_detail(movie['id'], actor_data)
                fields = {
                    'actors': details[1],
                    'genres': movie['genre_ids'],
                    'title': movie['title'],
                    'content': movie['overview'],
                    'release_date': movie['release_date'],
                    'runtime': details[0],
                    'rank': movie['vote_average'],
                    'poster_path': movie['poster_path'],
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("movie.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)

    with open("actor.json", "w", encoding="utf-8") as w:
        json.dump(actor_data, w, indent=4, ensure_ascii=False)
    
    print("Movie data has been successfully fetched and saved.")

# def get_movie_detail(movie_id, actor_data):
#     request_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits&language=ko-KR"
#     details = requests.get(request_url).json()
#     runtime = details['runtime']
#     actors = []

#     for cast in details['credits']['cast']:
#         if cast.get("known_for_department") == 'Acting':
#             actors.append(cast['id'])

#             fields = {
#                 'name': cast['original_name'],
#                 'profile_url': cast['profile_path']
#             }

#             data = {
#                 "pk": cast['id'],
#                 "model": "movies.actor",
#                 "fields": fields
#             }
            
#             actor_data.append(data)

#     return [runtime, actors]

# 배우 중복될 수 있으니...
def get_movie_detail(movie_id, actor_data):
    request_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits&language=ko-KR"
    details = requests.get(request_url).json()
    runtime = details['runtime']
    actors = []
    
    actor_ids = set([actor['pk'] for actor in actor_data])  # actor_data에 있는 모든 배우의 ID를 셋으로 만들어 중복을 방지합니다.

    for cast in details['credits']['cast']:
        if cast.get("known_for_department") == 'Acting' and cast['id'] not in actor_ids:  # 새로운 배우라면
            actors.append(cast['id'])
            actor_ids.add(cast['id'])  # 새로운 배우 ID를 셋에 추가합니다.

            fields = {
                'name': cast['original_name'],
                'profile_url': cast['profile_path']
            }

            data = {
                "pk": cast['id'],
                "model": "movies.actor",
                "fields": fields
            }
            
            actor_data.append(data)

    return [runtime, actors]


if __name__ == "__main__":
    get_movie_datas()
