<template>
  <div class="profile-page">
    <div class="navbar-container">
      <img
        :src="`https://api.dicebear.com/8.x/adventurer-neutral/svg?seed=${nickname}&radius=50`"
        alt="avatar"
        class="avatar"
      />
      <h3>{{ `${nickname}` }}</h3>
      <button v-if="!isMe" @click="subscribe">
        {{ isSubscribed ? '구독 취소' : '구독하기' }}
      </button>
      <nav>
        <RouterLink :to="{ name: 'myMovies', params: {userId: profileId} }">
          {{ `${nickname}님의 TOP 5 영화` }}
        </RouterLink>
        <RouterLink :to="{ name: 'notes', params: {userId: profileId} }">
          {{ `${nickname}님의 노트` }}
        </RouterLink>
        <RouterLink :to="{ name: 'watched', params: {userId: profileId} }">
          {{ `${nickname}님이 본 영화` }}
        </RouterLink>
        <RouterLink :to="{ name: 'towatch', params: {userId: profileId} }">
          {{ `${nickname}님이 볼 영화` }}
        </RouterLink>
        <div v-if="categories && categories.length > 3">
          <div v-for="(category, index) in categories.slice(3)" :key="index" class="category-link">
            <RouterLink 
              :to="{ name: 'category', params: {userId: profileId, categoryId: category.id} }" class="size">
              {{ `${category.name}` }}
            </RouterLink>
          </div>
        </div>
        <form @submit.prevent="addCategory">
          <div v-if="isMe" class="category-form">
            <label for="categoryName"> + </label>
            <input type="text" v-model.trim="name" id="categoryName" placeholder="카테고리명을 입력하세요.">
            <input type="submit" value="추가">
          </div>
        </form>
      </nav>
    </div>
    <div class="content">
      <RouterView :key="$route.fullPath"/>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const nickname = ref(null)
const store = useCounterStore()
const route = useRoute()

const profileId = route.params.userId
const userId = computed(() => store.currentUser.userId)
const categories = ref([])
const followings = ref([])
const followers = ref([])

const isMe = computed(() => Number(profileId) === Number(userId.value))
const isSubscribed = ref(false)

const getUserProfile = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/profile/${profileId}/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    nickname.value = response.data.nickname
    categories.value = response.data.my_categories
    followers.value = response.data.followers
    console.log('User profile loaded:', response.data)
    
    // Check if current user is subscribed to the profile user
    isSubscribed.value = followers.value.some(follower => {
      // console.log(`Comparing follower: ${Number(follower)} with userId: ${Number(userId.value)}`)
      return Number(follower) === Number(userId.value)
    })
    // console.log('isSubscribed:', isSubscribed.value)
  } catch (error) {
    console.log('Error loading user profile:', error)
  }
}

const subscribe = async function () {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/accounts/${profileId}/follow/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    if (response.data.is_following) {
      followers.value.push(Number(userId.value))
      isSubscribed.value = true
      console.log('구독 완료')
    } else {
      followers.value = followers.value.filter(follower => Number(follower.id) !== Number(userId.value))
      isSubscribed.value = false
      console.log('구독 취소')
    }
    console.log('Updated followers:', followers.value)
  } catch (error) {
    console.log('Subscription error:', error)
  }
}

const name = ref(null)

const addCategory = async function () {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/categories/user/${userId.value}/`,
      data: {
        name: name.value
      },
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    categories.value = [...categories.value, response.data]
    name.value = ''
  } catch (error) {
    console.log('Error adding category:', error)
  }
}

onMounted(async () => {
  await getUserProfile()
})
</script>


<style scoped>
.profile-page {
  display: flex;
}

.navbar-container {
  position: fixed;
  height: 100%;
  top: 60px;
  left: 0;
  width: 220px;
  background-color: #f8f9fa;
  padding: 20px;
  text-align: center;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 20px;
}

h3 {
  color: #4A90E2;
  margin-bottom: 20px;
}

button {
  display: block;
  width: 100%;
  margin-bottom: 20px;
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #357ABD;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 200px;
}

nav a {
  text-decoration: none;
  color: #4A90E2;
  margin: 10px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

nav a:hover {
  background-color: #4A90E2;
  color: white;
}

.category-link {
  padding: 10px;
}

.category-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px; /* 입력 폼 내의 요소들 사이에 일정한 간격을 줍니다 */
}

form input[type="text"] {
  width: calc(100% - 20px);
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

form input[type="submit"] {
  width: 100%;
  background-color: #4A90E2;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

form input[type="submit"]:hover {
  background-color: #357ABD;
}

.content {
  margin-left: 240px;
  padding: 20px;
  width: calc(100% - 240px);
}

.size {
  width: 100px;
  height: 100px;
}

</style>
