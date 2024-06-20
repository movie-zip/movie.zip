<template>
  <div class="followings-container">
    <h1 class="title">{{ nickname }}님이 구독한 유저</h1>
    <FollowingList
    v-for="following in followings.followings"
    :key="following.id"
    :following="following"/>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import FollowingList from '@/components/followings/FollowingList.vue'

const followings = ref([])
const store = useCounterStore()
const route = useRoute()
const userId = ref('')
const nickname = ref('')

// console.log(route.params.userId)
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/accounts/${route.params.userId}/followings/`,
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`
    }
  })
    .then((response) => {
      followings.value = response.data
      userId.value = route.params.userId
      console.log(userId.value)
      return axios({
        method: 'get',
        url: `${store.API_URL}/api/v1/accounts/profile/${userId.value}/`,
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
    })
    .then((response) => {
        nickname.value = response.data.nickname
    })
    .catch((error) => {
        console.log(error)
    })
})
</script>

<style scoped>
.followings-container {
  padding: 20px;
  background-color: #f0f4f8;
  border-radius: 8px;
}

.title {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

/* 추가적인 스타일링은 FollowingList 컴포넌트 내에서 진행될 수 있습니다. */
</style>
