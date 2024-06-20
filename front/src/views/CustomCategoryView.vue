<template>
  <div class="movie-category">
    <div class="header">
      <h2>{{ movieList.name }}</h2>
      <div class="icons" v-if="isMyCategory">
        <div class="icon-wrapper">
          <p @click="showEdit('editMode1')">
            <font-awesome-icon icon="pencil-alt" class="icon-gray" />
          </p>
          <div v-if="editMode1" class="edit-form">
            <form @submit.prevent="editCategory(1)">
              <label for="name1">카테고리명 :</label>
              <input id="name1" v-model="name" required />
              <button type="submit">제출</button>
            </form>
          </div>
          <p class="icon-container" @click="deleteCategory(1)">
            <font-awesome-icon icon="trash" class="icon-gray" />
          </p>
        </div>
      </div>
    </div>
    
    <div v-if="movieList && movieList.movies && movieList.movies.length">
      <Carousel :items-to-show="3" :wrap-around="true">
        <Slide v-for="movie in movieList.movies" :key="movie.id">
          <CategoryMovieListItem :movie="movie" />
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
import { ref, onMounted, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'
import CategoryMovieListItem from '@/components/movies/CategoryMovieListItem.vue'
import 'vue3-carousel/dist/carousel.css'
import { Carousel, Slide, Navigation } from 'vue3-carousel'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()
const movieList = ref([])
const categoryId = route.params.categoryId

const categoryUserId = ref(null)  // 카테고리 작성자의 id
const userId = computed(() => store.currentUser.userId)  // 현재 사용자의 id
const isMyCategory = computed(() =>  Number(userId.value) === Number(categoryUserId.value))
const name = ref('')
const editMode1 = ref(false)
const showEdit = (mode) => {
  if (mode === 'editMode1') {
    editMode1.value = !editMode1.value
    name.value = movieList.value.name  // 수정 버튼을 누르면 현재 카테고리 이름으로 초기화
  }
}

const getUserProfile = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/categories/${categoryId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    movieList.value = response.data
    categoryUserId.value = response.data.user
    // console.log(response.data)
  } catch (error) {
    console.log(error)
  }
}

// 카테고리명 수정
const editCategory = async (mode) => {
  try {
    await axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/categories/${route.params.categoryId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      },
      data: {
        name: name.value
      }
    })
    console.log('카테고리명 수정 완료')
    if (mode === 1) {
      editMode1.value = false
    }
    router.go(0)  // 브라우저의 새로 고침 버튼을 누르는 것과 유사한 효과
  } catch (err) {
    console.error('Error deleting note:', err)
  }
}

// 카테고리 삭제
const deleteCategory = async (mode) => {
  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/categories/${route.params.categoryId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    router.push({ name: 'myMovies', params: { userId : categoryUserId.value } })
} catch (err) {
console.error('Error deleting note:', err)
}
}

onMounted(async () => {
  await getUserProfile()
})
</script>

<style scoped>
.movie-category {
  margin: 20px;
}

.header {
  display: grid;
  /* grid-template-columns: 1fr 7fr 2fr; */
  text-align: center;
  align-items: center;
}

h2 {
  font-family: 'sweet6';
  color: #5197e2;
  margin-bottom: 16px;
  font-size: 24px;
  text-align: center;
}

input {
  margin-top: 5px;
  border: 1px solid #ccc;
}

.icons {
  display: flex;
  gap: 10px;
  justify-self: end;
  position: relative; /* Ensures absolute positioning within this container */
}

.icon-wrapper {
  position: relative;
}

.edit-form {
  position: absolute;
  top: 0;
  left: calc(100% + 10px);
  transform: translateX(-100%);
  background: white;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  z-index: 10;
}

.edit-form button {
  margin-top: 10px;
  background-color: #808080; /* 회색 배경 */
  color: white; /* 흰색 텍스트 */
  border: none; /* 테두리 없음 */
}

.icon-container {
  cursor: pointer;
}

.no-movies {
  font-size: larger;
  text-align: center;
  margin-top: 20px;
  color: #888;
}

h2 {
  margin-top: 40px;
  text-align: center;
  font-family: 'sweet6';
  color: #4A90E2

}

.hover-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0); /* Transparent background by default */
  transition: background-color 0.3s ease; /* Smooth transition effect */
  z-index: 5; /* Ensure the hover effect is below the icons */
}

.icons:hover .hover-effect {
  background-color: rgba(0, 0, 0, 0.1); /* Semi-transparent black background on hover */
}

.movie-poster {
  width: 200px; /* 이미지의 최대 너비를 150px로 설정 */
  height: 300px; /* 이미지의 높이를 자동으로 조정하여 비율을 유지 */
  border-radius: 8px;
}

.edit-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-gray {
  color: rgb(210, 210, 210);
}
</style>
