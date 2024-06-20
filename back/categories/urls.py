from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:user_pk>/', views.category_list),  # category 생성 / 리스트 조회
    path('<int:category_pk>/', views.category_detail),    # 특정 카테고리 수정, 삭제, 카테고리 detail 조회
    path('<int:category_pk>/update/<int:movie_pk>/', views.category_update),  # 특정 카테고리에 영화 추가
]
