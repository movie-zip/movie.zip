<template>
  <div>
    <RouterLink :to="{name:'MovieDetailView', params:{movieId:movie.id}}" class="link">
      <div>
        <h4>{{ movie.title }}</h4>
        <p class="icon-container" v-if="isMyCategory" @click.stop.prevent="deleteMovie">
          <font-awesome-icon icon="trash" class="icon-gray"/>
        </p>
        <img
          class="movie-poster"
          :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
          alt="movie_poster">
      </div>
    </RouterLink>  
  </div>
</template>

<script setup>
import axios from 'axios'
import { defineProps, computed, ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  movie: Object
})
const route = useRoute()
const router = useRouter()
const store = useCounterStore()
const movieList = ref([])
const userId = computed(() => store.currentUser.userId)  // 내 id
// console.log(` 내 userId : ${userId.value}`)
const categoryUserId = route.params.userId   // 현재 방문한 카테고리의 유저 id
// console.log(categoryUserId) // 잘 나옴
const categoryId = ref(null)
const isMyCategory = computed(() =>  Number(userId.value) === Number(categoryUserId))
// console.log(`카테고리아이디: ${categoryId}`)

const getUserCategory = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/categories/20/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    // console.log(response.data)
    movieList.value = response.data.movies
  } catch (error) {
    console.log(error)
  }
}

// const getUserInfo 머 이런 걸로 그 사람의 카테고리 목록을 가져옴. 
// 여기는 볼 영화니까 두 번쨰 카테고리가 곧 지금의 categoryId
const getUserProfile = async () => {  // 현재 들어간 프로필 사용자의 정보를 가져온다
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/profile/${categoryUserId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    // console.log(response.data.my_categories[0].id)
    categoryId.value = response.data.my_categories[1].id  // 현재 들어간 카테고리 아이디
  } catch (error) {
    console.log(error)
  }
}

const movieId = props.movie.id
// console.log(`무비아이디: ${movieId}`)
const deleteMovie = async () => {
  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/categories/${categoryId.value}/update/${movieId}`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    const index = movieList.value.findIndex(m => m.id === movieId)
    if (index !== -1) {
      movieList.value.splice(index, 1)
    }
    router.go(0)
    await getUserProfile()
  } catch (err) {
    console.error('Error deleting note:', err)
  }
}

onMounted(async () => {
  await getUserProfile()
  await getUserCategory()
})
</script>

<style scoped>
.movie-poster {
  width: 200px; /* 이미지의 최대 너비를 300px로 설정 */
  height: 300px; /* 이미지의 높이를 자동으로 조정하여 비율을 유지 */
  border-radius: 8px;
}

.link {
  text-decoration: none;
  color:#5197e2;
}
</style>