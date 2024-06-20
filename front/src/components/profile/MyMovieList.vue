<template>
  <div>
    <h1 class="nickname">{{ nickname }}'s PICK</h1>
    <hr>
    <div v-if="movies && movies.length">
      <Carousel :items-to-show="3" :wrap-around="true">
        <Slide v-for="movie in movies" :key="movie.id">
          <MyMovieListItem :movie="movie" />
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
import MyMovieListItem from '../movies/MyMovieListItem.vue'
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
    categoryId.value = response.data.my_categories[0].id  // 현재 들어간 카테고리 아이디
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
div {
  padding: 20px;
  background-color: rgb(255, 253, 239);
  border-radius: 8px;
  align-content: center;
  align-items: center;
}

h2 {
  font-family: 'sweet6';
  color: #5197e2;
  margin-bottom: 16px;
  font-size: 24px;
  text-align: center;
}

.my-movie-list-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 12px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.my-movie-list-item img {
  width: 80px;
  height:auto;
  border-radius: 8px;
  margin-right: 16px;
}

.my-movie-list-item .movie-info {
  display: flex;
  flex-direction: column;
}

.no-movies {
  font-size: larger;
  text-align: center;
  margin-top: 20px;
  color: #888;
}
</style>