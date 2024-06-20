from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # movie
    # 영화 검색
    path('search/', views.search_movie, name='search_movie'), 
    # 영화 상세 정보 조회
    path('<int:movie_id>/detail/', views.search_and_get_movie_detail, name='movie_detail'),
    # 영화 평점 등록
    path('<int:movie_id>/rating/', views.create_rating, name='create_rating'),
    # 영화 평점 삭제
    path('<int:movie_pk>/rating/<int:rating_pk>/', views.rating_update_or_delete, name='rating_update_or_delete'),
    # 영화 추천
    path('recommendation/', views.recommend_movies, name='recommend_movies'),
]