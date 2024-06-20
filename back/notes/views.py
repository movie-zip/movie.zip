from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import NoteSerializer, NoteListSerializer, CommentSerializer, FollowingNoteSerializer
from .models import Note, Comment
from movies.models import Movie

User = get_user_model()
# 노트 상세 페이지에서 글을 수정 권한 여부 확인 시 필요
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
    })
    
@api_view(['GET'])
def note_list(request, user_pk): # 해당 유저가 작성한 모든 note 목록 조회       
    notes = get_list_or_404(Note.objects.order_by('-created_at'), user_id=user_pk)
    serializer = NoteListSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])  # 완
@permission_classes([IsAuthenticated])
def following_note_list(request):      # 내가 구독한 유저들이 작성한 note 목록 조회
    user = get_object_or_404(User, pk=request.user.pk)
    following_users = user.followings.all()
    notes = Note.objects.filter(user__in=following_users).order_by('-created_at')
    serializer = FollowingNoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])      # 완
def movie_note_list(request, user_pk, movie_pk): # 해당 유저가 작성한 특정 영화에 대한 모든 note 조회  
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, pk=user_pk)
    # 해당 유저가 작성한 특정 영화에 대한 모든 노트 가져오기
    notes = Note.objects.filter(movie=movie, user=user)
    serialzer = NoteSerializer(notes, many=True)
    return Response(serialzer.data, status=status.HTTP_200_OK)

# 특정 영화에 대해 나를 제외한 모든 유저들의 노트 조회    
@api_view(['GET'])
def other_users_movie_notes(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    current_user = request.user

    # 현재 로그인한 사용자가 작성한 노트를 제외한 나머지 노트 가져오기
    notes = Note.objects.filter(movie=movie).exclude(user=current_user)
    serializer = NoteListSerializer(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 노트 작성
@api_view(['POST'])         # 완
def create_note(request, movie_pk): 
    movie = get_object_or_404(Movie, pk=movie_pk)
    # print(movie)
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=401)
    
        user_id = request.user.id
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    if request.method == 'GET':     # note 상세 조회
        serializer = NoteSerializer(note)
        return Response(serializer.data) 
    
    elif request.method == 'PUT':   # note 수정
        serializer = NoteSerializer(instance=note, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':    # note 삭제
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 댓글 작성 
@api_view(['POST'])
def create_comment(request, note_pk):
    user = request.user
    note = get_object_or_404(Note, pk=note_pk)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(note=note, user=user)

        # 기존 serializer 가 return 되면, 단일 comment 만 응답으로 받게됨.
        # 사용자가 댓글을 입력하는 사이에 업데이트된 comment 확인 불가 => 업데이트된 전체 목록 return 
        comments = note.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# 댓글 수정 삭제 기능
@api_view(['PUT', 'DELETE'])
def comment_update_or_delete(request, note_pk, comment_pk):
    note = get_object_or_404(Note, pk=note_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    def update_comment():
        if request.user == comment.user:
            serializer = CommentSerializer(instance=comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                comments = note.comments.all()
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

    def delete_comment():
        if request.user == comment.user:
            comment.delete()
            comments = note.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
    
    if request.method == 'PUT':
        return update_comment()
    elif request.method == 'DELETE':
        return delete_comment()
    
