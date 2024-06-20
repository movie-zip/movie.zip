from django.urls import path, include
from . import views

urlpatterns = [
    path('my_profile/', views.get_user_info),  # token으로 userId 찾기
    path('profile/<int:user_pk>/', views.get_profile),  # profile 조회
    path('<int:user_pk>/follow/',views.follow),
    path('<int:user_pk>/followings/', views.get_followings),
    path('get_user_obj/', views.get_user_obj),
]