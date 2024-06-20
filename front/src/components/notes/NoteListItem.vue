<template>
  <div class="item" @mouseover="isHovered = true" @mouseleave="isHovered = false">
    <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: props.note.movie.id } }" class="link">
      <div class="movie-info" @mouseover="isMovieHovered = true" @mouseleave="isMovieHovered = false">
        <h3>{{ props.note.movie.title }}</h3>
        <img 
          class="movie-poster" 
          :src="`https://image.tmdb.org/t/p/w500/${props.note.movie.poster_path}`" 
          :alt="`${props.note.movie.title} 포스터`"  
        >
      </div>
    </RouterLink>
    <RouterLink :to="{ name: 'NoteDetailView', params: { noteId: props.note.id } }" class="link">    
      <p class="note-content" @mouseover="isNoteHovered = true" @mouseleave="isNoteHovered = false">
        {{ truncatedContent }}
      </p>
    </RouterLink>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  note: Object
});

const isHovered = ref(false);
const isMovieHovered = ref(false);
const isNoteHovered = ref(false);

const truncatedContent = computed(() => {
  const maxLength = 100; // 노트 내용의 최대 길이 설정
  return props.note.content.length > maxLength 
    ? props.note.content.substring(0, maxLength) + '...' 
    : props.note.content;
});
</script>

<style scoped>
div {
  color: #5197e2;
}

.item {
  width: 200px;
  height: 600px;
  transition: transform 0.3s ease;
  transform: scale(1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.item:hover {
  transform: scale(1.05);
}

.movie-info {
  transition: transform 0.3s ease;
  transform: scale(1);
  text-align: center;
}
.movie-info:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 200px; 
  height: 300px;
  border-radius: 8px;
}

.note-content {
  height: 150px; /* 고정 높이 설정 */
  overflow: hidden; /* 오버플로우 숨기기 */
  text-overflow: ellipsis; /* 텍스트가 넘칠 경우 ... 표시 */
  display: -webkit-box;
  -webkit-line-clamp: 10; /* 텍스트가 10줄을 넘지 않도록 설정 */
  -webkit-box-orient: vertical;
  transition: transform 0.3s ease;
  transform: scale(1);
}
.note-content:hover {
  transform: scale(1.1);
}

.link {
  text-decoration: none;
  color: #5197e2;
}
</style>
