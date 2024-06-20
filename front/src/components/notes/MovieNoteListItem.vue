<template>
    <div class="note-item">
      <!-- 사용자 프로필 -->
      <div class="user-profile">
        <!-- 사용자 프로필 이미지 추가 -->
        <img 
          :src="`https://api.dicebear.com/8.x/adventurer-neutral/svg?seed=${note.user.nickname}&radius=50`" 
          alt="유저 프로필" 
          class="user-avatar"
        />
        <RouterLink :to="{ name: 'ProfileView', params: { userId:`${note.user.user_id}`}}" class="link">
          <h3 class="user-nickname"><span>{{note.user.nickname}}</span></h3>
        </RouterLink>
      </div>
  
      <!-- 노트 내용 -->
      <RouterLink :to="{name:'NoteDetailView', params: {noteId:`${note.id}`}}" class="link">
        <p class="note-content"><span>{{ note.content }}</span></p>
      </RouterLink>
      <!-- <hr> -->
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router';
  import { defineProps } from 'vue';
  
  const props = defineProps({
    note: {
      type: Object,
      required: true
    }
  });
  </script>
  
  <style scoped>
  .note-item {
    width: 800px; /* 최대 너비 설정 */
    background-color: rgb(255, 253, 239); /* 배경색 설정 */
    border-radius: 8px; /* 테두리 둥근 처리 */
    padding: 20px; /* 내부 여백 설정 */
    margin: 20px 0; /* 상하 여백 설정 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 상자 그림자 효과 */
    transition: transform 0.5s ease, box-shadow 0.5s ease; /* 부드러운 전환 효과 */
  }
  
  .note-item:hover {
    transform: scale(1.05); /* 호버 시 전체 노트 아이템 약간 확대 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 강조 */
  }
  
  .user-profile {
    display: flex;
    align-items: center;
    gap: 20px; /* 이미지와 닉네임 간의 간격 */
  }
  
  .user-avatar {
    width: 30px; /* 이미지 크기 */
    height: 30px; /* 이미지 크기 */
    border-radius: 50%; /* 원형 이미지 */
    transition: transform 0.5s ease; /* 부드러운 전환 효과 */
  }
  
  .user-profile:hover .user-avatar,
  .user-profile:hover .user-nickname {
    transform: scale(1.5); /* 호버 시 프로필 이미지와 유저 닉네임 확대 */
  }
  
  .user-nickname {
    color: #5197e2; /* 유저 닉네임 색상 설정 */
    margin: 10px 0; /* 유저 닉네임 상하 여백 설정 */
    transition: transform 0.5s ease; /* 부드러운 전환 효과 */
    transform-origin: left top; /* 확대 중심을 좌측 상단으로 설정 */
  }
  
  .note-content {
    color: #405957; /* 노트 내용 색상 설정 */
    line-height: 1.5; /* 줄 간격 설정 */
    transition: transform 0.5s ease; /* 부드러운 전환 효과 */
    transform-origin: left top; /* 확대 중심을 좌측 상단으로 설정 */
    text-decoration: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .note-content:hover {
    transform: scale(1.5); /* 호버 시 노트 내용 확대 */
  }
  
  .link {
    text-decoration: none; /* 링크 밑줄 제거 */
  }
  
  hr {
    border: none; /* 기본 테두리 제거 */
    border-top: 1px solid #eee; /* 상단 테두리만 설정 */
    margin: 20px 0; /* 상하 여백 설정 */
  }
  </style>
  