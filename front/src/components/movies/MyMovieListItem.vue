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
const categoryUserId = route.params.userId   // 현재 방문한 카테고리의 유저 id
const categoryId = ref(null)
const isMyCategory = computed(() =>  Number(userId.value) === Number(categoryUserId))
const movieId = props.movie.id
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
    categoryId.value = response.data.my_categories[0].id  // 현재 들어간 카테고리 아이디
  } catch (error) {
    console.log(error)
  }
}

const getMovies = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/categories/${categoryId.value}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    movieList.value = [...response.data.movies]
  } catch (error) {
    console.log(error)
  }
}

const deleteMovie = async () => {
  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/categories/${categoryId.value}/update/${movieId}`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    });
    // Delete successful, remove the movie from the list
    const index = movieList.value.findIndex(m => m.id === movieId)
    if (index !== -1) {
      movieList.value.splice(index, 1)
    }
    await getUserCategory()
    router.go(0)
  } catch (error) {
    console.log(error);
  }
};

onMounted(async () => {
  await getUserProfile()
  await getUserCategory()
})
</script>

<style scoped>
.movie-poster {
  width: 200px;
  height: 300px; /* 이미지의 비율을 유지하면서 높이 설정 */
  transition: transform 0.3s ease; /* 이미지에 부드러운 트랜지션 효과 추가 */
  border-radius: 8px;
}

.subscription-title {
  text-align: center; /* 텍스트 중앙 정렬 */
  color: #5197e2; /* 글자색 설정 */
}

.link {
  text-decoration: none;
  color:#5197e2;
}
</style>