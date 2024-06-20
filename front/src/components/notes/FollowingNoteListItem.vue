<template>
  <div class="note-item">
    <!-- 포스터 컨테이너 -->
    <div class="poster-container">
      <RouterLink :to="{name:'MovieDetailView', params: { movieId:`${note.movie.id}` } } " class="link">
        <img class="movie-poster"
             :src="`https://image.tmdb.org/t/p/w500/${note.movie.poster_path}`"
             alt="영화 포스터">
      </RouterLink>
    </div>
    
    <!-- 텍스트 컨테이너 -->
    <div class="text-container">
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
      <RouterLink :to="{name:'NoteDetailView', params: {noteId:`${note.id}`}}" class="link">
        <p class="note-content"><span>{{ note.content }}</span></p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter, RouterLink } from 'vue-router';

const props = defineProps({
  note: {
    type: Object,
    required: true
  }
})

const router = useRouter();
</script>

<style scoped>
.user-profile {
  display: flex;
  align-items: center;
  gap: 20px; /* 이미지와 닉네임 간의 간격 */
}

.user-avatar {
  width: 30px; /* 이미지 크기 */
  height: 30px; /* 이미지 크기 */
  border-radius: 50%; /* 원형 이미지 */
}

.note-item {
  display: flex; /* Flexbox 적용 */
  align-items: flex-start; /* 항목들을 상단 정렬 */
  gap: 20px; /* 이미지와 텍스트 컨테이너 사이 간격 */
  background-color: rgb(255, 253, 239); /* 배경색 설정 */
  border-radius: 8px; /* 테두리 둥근 처리 */
  padding: 20px; /* 내부 여백 설정 */
  margin: 20px 0; /* 상하 여백 설정 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 상자 그림자 효과 */
  transition: transform 0.5s ease, box-shadow 0.5s ease; /* 부드러운 전환 효과 */
}

.note-item:hover {
  transform: scale(1.01); /* 호버 시 전체 노트 아이템 약간 확대 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 강조 */
}

.movie-poster {
  width: 200px; /* 이미지의 최대 너비를 200px로 설정 */
  height: auto; /* 이미지의 높이를 자동으로 조정하여 비율을 유지 */
  display: block; /* 블록 레벨 요소로 설정 */
  border-radius: 20px; /* 이미지 둥근 처리 */
  margin: 10px 0; /* 상하 여백 설정 */
  padding: 10px ;
  transition: transform 0.5s ease; /* 부드러운 전환 효과 */
}

.movie-poster:hover {
  transform: scale(1.1); /* 호버 시 이미지 확대 */
}

.text-container {
  flex: 1 1 auto; /* 텍스트 컨테이너는 남은 공간을 모두 차지 */
}

.user-nickname, .note-content, .user-avatar {
  transition: transform 0.5s ease; /* 부드러운 전환 효과 */
  transform-origin: left top; /* 확대 중심을 좌측 상단으로 설정 */
}

.user-profile:hover .user-avatar,
.user-profile:hover .user-nickname {
  transform: scale(1.3); /* 호버 시 프로필 이미지와 유저 닉네임 확대 */
}

.note-content:hover {
  transform: scale(1.3); /* 호버 시 노트 내용 확대 */
}

.link {
  text-decoration: none; /* 링크의 기본 밑줄 제거 */
}

h3 {
  color: #5197e2; /* 제목 색상 설정 */
  margin: 10px 0; /* 제목 상하 여백 설정 */
}

p {
  color: #5197e2; /* 문단 색상 설정 */
  line-height: 1.5; /* 줄 간격 설정 */
}
</style>
