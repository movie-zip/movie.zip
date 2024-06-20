<template>
  <div class="content-container">
    <div class="following-list">
      <FollowingList :followings="followings" />
    </div>
    <div class="following-notes">
      <FollowingNoteList :notes="notes" />
    </div>
    <div class="movie-recommend">
      <MovieRecommend />
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import FollowingNoteList from '@/components/notes/FollowingNoteList.vue';
import MovieRecommend from '@/components/movies/MovieRecommend.vue';
import FollowingList from '@/components/followings/FollowingList.vue';
import axios from 'axios';
import { ref, onMounted, computed, watch } from 'vue';

const store = useCounterStore();
const notes = ref([]);
const followings = ref([]);

// 타임라인
const getFollowingNoteList = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/notes/following/list/`,
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    }
  })
    .then(response => {
      notes.value = response.data;
    })
    .catch(err => console.error(err));
};
const userId = computed(() => store.currentUser.userId);

// 내가 구독하고 있는 유저 목록
const getFollowingList = () => {
  if (userId.value) {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/accounts/${userId.value}/followings/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
      .then(response => {
        followings.value = response.data;
      })
      .catch(err => console.error(err));
  }
};

onMounted(async () => {
  await store.getUserObj();
  getFollowingList();
  getFollowingNoteList();
});

// Watch for userId changes and refetch followings
watch(userId, (newUserId) => {
  if (newUserId) {
    getFollowingList();
  }
});
</script>

<style scoped>
.content-container {
  display: flex;
  justify-content: space-between; /* 항목들을 양쪽 끝으로 배치 */
  align-items: flex-start; /* 아이템들이 상단에 정렬되도록 함 */
  max-width: 1200px; /* 전체 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
}

.following-list, .following-notes, .movie-recommend {
  display: flex;
  flex-direction: column; /* 하위 항목들을 위에서 아래로 정렬 */
  gap: 20px; /* 하위 항목들 사이의 간격 */
}

.following-list {
  flex: 1; /* 팔로잉 리스트를 왼쪽에 배치 */
  max-width: 200px; /* 최대 너비 제한을 줄임 */
  margin-right: auto; /* 오른쪽 여백 자동 조정 */
}

.following-notes {
  flex: 2; /* 팔로잉 노트 리스트를 중앙에 배치 */
  max-width: 800px; /* 최대 너비 제한을 넓힘 */
  margin: 0 20px; /* 중앙 정렬 */
}

.movie-recommend {
  flex: 1; /* 영화 추천을 오른쪽에 배치 */
  max-width: 200px; /* 최대 너비 제한을 줄임 */
  margin-left: auto; /* 왼쪽 여백 자동 조정 */
}

.following-list > *, .following-notes > *, .movie-recommend > * {
  background-color: rgb(255, 253, 239);
}
</style>
