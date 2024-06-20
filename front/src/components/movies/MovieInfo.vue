<template>
  <div class="movie-details-container">
    <h2 class="movie-title">영화 상세 정보</h2>
    <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" alt="" class="movie-poster">
    <p><h3 class="movie-detail">영화 제목 : {{ movie.title }}</h3></p>
    <h4 class="movie-detail">영화 장르 : 
      <span v-for="(genre, index) in movie.genres" :key="genre.id">
        {{ genre.name }}<span v-if="index < movie.genres.length - 1">, </span>
      </span>
    </h4>
    <h4 class="movie-detail">영화 배우 : 
      <span v-for="(actor, index) in limitedActors" :key="actor.id">
        {{ actor.name }}<span v-if="index < limitedActors.length - 1">, </span>
      </span>
    </h4>
    <h4 class="movie-detail">영화 줄거리 : {{ movie.content }}</h4>
    <h4 class="movie-detail">영화 평점: {{ movie.rank }}점</h4>
    <h4 class="movie-detail">영화 상영시간: {{ movie.runtime }}분</h4>
    <h4 class="movie-detail">영화 개봉일자: {{ movie.release_date }}</h4>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { defineProps } from 'vue';
import { computed } from 'vue';

const store = useCounterStore()

const props = defineProps({
  movie: Object
});
const limitedActors = computed(() => {
  return props.movie && props.movie.actors ? props.movie.actors.slice(0, 10) : [];
});
</script>

<style scoped>
.movie-details-container {
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: rgb(255, 253, 239); /* 배경색 추가 */
  max-width: 800px; /* 최대 너비 설정 */
  margin: 0 auto; /* 좌우 가운데 정렬 */
  text-align: center; /* 텍스트 가운데 정렬 */
}

.movie-title {
  color: #4A90E2;
  font-size: 2em;
  margin-bottom: 20px;
}

.movie-poster {
  width: 100%;
  max-width: 400px; /* 최대 너비 설정 */
  margin: 20px auto; /* 가운데 정렬을 위해 자동 여백 */
  display: block; /* block 요소로 변경하여 가운데 정렬 */
}

.movie-detail {
  color: #4A90E2;
  font-size: 1.2em;
  margin: 10px 0;
}

/* 영화 장르와 배우 리스트의 세부 스타일 */
.movie-detail span {
  color: #4A90E2
}
</style>
