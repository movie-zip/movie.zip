<template>
  <div class="movie-recommendations">
    <h2 class="title">영화 추천</h2>
    <ol class="movie-list">
      <div v-if="isLoading">Loading...</div>
      <template v-else>
        <MovieRecommendList 
          v-for="movie in movielist.recommended_movies"
          :key="movie.id"
          :movie="movie" 
        />
      </template>
    </ol>
  </div>
</template>

<script setup>
import MovieRecommendList from '@/components/movies/MovieRecommendList.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const movielist = ref([])
const isLoading = ref(true)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/movies/recommendation/`,
    headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
    }
  })
  .then(res => {
    movielist.value = res.data
    isLoading.value = false
  })
  .catch(err => {
    // 에러 처리
    isLoading.value = false
  })
})
</script>

<style scoped>
.movie-recommendations {
  margin-top: 40px; /* 내브바와의 간격 */
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  
}

.title {
  margin-bottom: 20px;
  color: #5197e2;
  text-align: center;
}

.movie-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.movie-list li {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: transform 0.2s ease-in-out;
}

.movie-list li:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
