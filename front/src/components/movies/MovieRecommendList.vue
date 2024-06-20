<template>
  <div>
    <li>
      <div class="movie-container">
        <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: `${movie.movie_id}` } }" class="link">
          <h4 class="movie-title">{{ movie.title }}</h4>
          <img
            class="movie-poster"
            :src="movie.poster_path"
            :alt="`${movie.title} 포스터`"> <!-- alt 속성을 통해 접근성 향상 -->
        </RouterLink>
      </div>
    </li>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  movie: Object // 영화 정보를 나타내는 객체를 props로 받음
})
</script>

<style scoped>
.movie-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px; /* 포스터 간의 간격을 조절하기 위해 마진 추가 */
}

.movie-title {
  color: #5197e2;
  transition: transform 0.5s; /* 부드러운 변환 효과 */
}

.movie-poster {
  max-width: 200px; /* 이미지의 최대 너비를 200px로 설정 */
  height: auto; /* 이미지의 높이를 자동으로 조정하여 비율을 유지 */
  border-radius: 10px; /* 포스터의 모서리를 둥글게 처리하여 디자인 개선 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* 포스터에 그림자 효과 추가 */
  transition: transform 0.5s; /* 부드러운 변환 효과 */
}

.link {
  text-decoration: none; /* 링크의 기본 밑줄 제거 */
  text-align: center;
}

.movie-title:hover, .movie-poster:hover {
  transform: scale(1.1); /* 호버 시 크기를 1.1배로 확대 */
}
</style>
