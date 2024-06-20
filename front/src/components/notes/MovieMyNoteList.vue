<template>
  <div class="note-container">
    <!-- 영화 노트의 상세 정보 제목 -->
    
    <ul>
      <!-- notes 배열의 각 항목에 대해 리스트 아이템 생성 -->
      <li v-for="note in notes" :key="note.id" class="note-item">
        <!-- 각 노트 상세 페이지로의 링크. note.id를 파라미터로 사용 -->
        <RouterLink 
          :to="{name: 'NoteDetailView', params: { noteId: `${note.id}` } }" 
          class="note-link"
        >
          <!-- 노트 내용 표시 -->
          <p class="note-content">{{ note.content }}</p>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

// props 정의. notes 배열 받기
const props = defineProps({
  notes: Array
});
</script>

<style scoped>
/* 컨테이너 스타일 */
.note-container {
  font-family: 'sweet6';
  background-color: rgb(255, 253, 239); /* 배경색 설정 */
  padding: 20px; /* 내부 여백 설정 */
  border-radius: 8px; /* 둥근 모서리 설정 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 상자 그림자 설정 */
  max-width: 800px; /* 최대 너비 설정 */
  margin: 0 auto; /* 가운데 정렬 */
}

/* 제목 스타일 */
h2 {
  color: #4A90E2; /* 제목 색상 설정 */
  margin-bottom: 15px; /* 제목과 목록 사이의 여백 설정 */
  text-align: center; /* 제목 가운데 정렬 */
  font-size: medium;
}

/* 목록 스타일 */
ul {
  list-style-type: none; /* 목록 스타일 제거 */
  padding: 0; /* 목록의 내부 여백 제거 */
}

/* 목록 항목 스타일 */
.note-item {
  background-color: rgb(248, 247, 235); /* 목록 항목 배경색 설정 */
  border-radius: 8px; /* 둥근 모서리 설정 */
  padding: 20px; /* 내부 여백 설정 */
  margin: 20px 0; /* 상하 여백 설정 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 상자 그림자 효과 */
  transition: transform 0.5s ease, box-shadow 0.5s ease; /* 부드러운 전환 효과 */
}

.note-item:hover {
  transform: scale(1.05); /* 호버 시 전체 노트 아이템 약간 확대 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 강조 */
}

/* 문단 스타일 */
.note-content {
  color: #4A90E2; /* 노트 내용 색상 설정 */
  line-height: 1.5; /* 줄 간격 설정 */
  transition: transform 0.5s ease; /* 부드러운 전환 효과 */
  transform-origin: left top; /* 확대 중심을 좌측 상단으로 설정 */
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.note-item:hover {
  transform: scale(1.05); /* 호버 시 전체 노트 아이템 약간 확대 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* 호버 시 그림자 강조 */
}

/* 링크 스타일 */
.note-link {
  text-decoration: none; /* 링크 밑줄 제거 */
  color: inherit; /* 링크 색상 상속 */
}

</style>
