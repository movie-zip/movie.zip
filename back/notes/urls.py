from django.urls import path
from . import views

urlpatterns = [
  # 노트
  path('<int:movie_pk>/', views.create_note),
  path('<int:user_pk>/list/', views.note_list),
  path('following/list/', views.following_note_list),
  path('<int:user_pk>/list/<int:movie_pk>/', views.movie_note_list),
  path('other/list/<int:movie_pk>/', views.other_users_movie_notes),
  path('<int:note_pk>/detail/', views.note_detail),
  path('users/me/', views.current_user),
  # 댓글
  path('<int:note_pk>/comment/', views.create_comment),
  path('<int:note_pk>/comment/<int:comment_pk>/', views.comment_update_or_delete),
]