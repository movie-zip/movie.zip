<template>
  <div>
    <h1 class="nickname">{{ nickname }}님이 본 영화</h1>
    <hr>
    <div v-if="movies && movies.length">
      <Carousel :items-to-show="3" :wrap-around="true">
        <Slide v-for="movie in movies" :key="movie.id">
          <WatchedMovieListItem :movie="movie" />
        </Slide>
        <template #addons>
          <Navigation />
        </template>
      </Carousel>
    </div>
    <div v-else class="no-movies">
      영화를 추가해주세요
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import WatchedMovieListItem from '@/components/movies/WatchedMovieListItem.vue'
import 'vue3-carousel/dist/carousel.css'
import { Carousel, Slide, Navigation } from 'vue3-carousel'

const store = useCounterStore()
const movies = ref([])
const route = useRoute()
const profileId = route.params.userId
const nickname = ref('')
const categoryId = ref(null)

const getUserProfile = async () => {  // 현재 들어간 프로필 사용자의 정보를 가져온다
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/profile/${profileId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    nickname.value = response.data.nickname
    categoryId.value = response.data.my_categories[1].id  // 현재 들어간 카테고리 아이디
  } catch (error) {
    console.log(error)
  }
}

const getCategoryInfo = async () => {  // 현재 들어간 프로필 사용자의 정보를 가져온다
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/categories/${categoryId.value}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    // console.log(response.data.movies)
    movies.value = response.data.movies  
  } catch (error) {
    console.log(error)
  }
}

onMounted(async () => {
  await getUserProfile()
  getCategoryInfo()
})
</script>

<style scoped>
/* 닉네임 스타일 */
h1.nickname {
  font-size: 24px; /* 폰트 크기 */
  color: #4A90E2; /* 글자 색상 */
  margin-top: 45px;
  margin-bottom: 20px; /* 아래 여백 */
  text-align: center; /* 중앙 정렬 */
}

/* 구분선 스타일 */
hr {
  border: 0;
  height: 2px;
  background: #ccc; /* 구분선 색상 */
  margin-bottom: 30px; /* 아래 여백 */
}


/* Slide 아이템 스타일 */
.slide {
  padding: 10px; /* 패딩 추가 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
  border-radius: 10px; /* 모서리 둥글게 */
  background: #fff; /* 배경색 */
}

/* Navigation 버튼 스타일 */
.navigation {
  display: flex;
  justify-content: center; /* 중앙 정렬 */
  margin-top: 20px; /* 위 여백 */
}

.navigation button {
  background: #007bff; /* 버튼 배경색 */
  color: #fff; /* 버튼 글자색 */
  border: none; /* 테두리 제거 */
  padding: 10px 15px; /* 패딩 */
  margin: 0 5px; /* 양쪽 여백 */
  border-radius: 5px; /* 모서리 둥글게 */
  cursor: pointer; /* 커서 포인터 */
}

.navigation button:hover {
  background: #0056b3; /* 호버시 배경색 */
}

.no-movies {
  font-size: larger;
  text-align: center;
  margin-top: 20px;
  color: #888;
}
</style>
