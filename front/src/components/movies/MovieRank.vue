<template>
  <div class="rating-container">
    <h2 class="rating-title">영화 평가 등록하기</h2>
    <p v-if="ratinggg" class="rating-display">평점: {{ ratinggg }}</p>
    <form @submit.prevent="submitRating" class="rating-form">
      <label for="rating" class="rating-label">평점을 입력하세요</label>
      <input type="number" id="rating" v-model.number="rating" min="1" max="10" required class="rating-input">
      <button type="submit" class="rating-button">등록하기</button>
    </form>
    <button v-if="ratingId" @click="deleteRating" class="rating-delete-button">평점 삭제하기</button>
    <div class="button-spacing"></div> <!-- 버튼 간격을 조절하기 위한 빈 요소 추가 -->
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter.js';

const store = useCounterStore();
const route = useRoute();
const rating = ref(null);
const ratinggg = ref('');
const ratingId = ref(null);

const props = defineProps({
  movie: Object
});

const fetchRating = (movieId) => {
  axios.get(`/api/v1/movies/${movieId}/rating/`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('token')}`
    }
  })
  .then(response => {
    if (response.data.length > 0) {
      ratinggg.value = response.data[0].rate;
      ratingId.value = response.data[0].id;
    } else {
      ratinggg.value = ''; // 평점이 없는 경우 초기화
      ratingId.value = null; // ratingId도 초기화
    }
  })
  .catch(error => {
    console.error('평가 가져오기 에러:', error);
  });
};

const submitRating = () => {
  const movieId = route.params.movieId;
  const requestData = {
    rate: rating.value
  };

  axios.post(
    `${store.API_URL}/api/v1/movies/${movieId}/rating/`, 
    requestData,
    {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    }
  )
  .then(response => {
    console.log('평가 등록 완료:', response.data);
    ratinggg.value = response.data.rate;
    ratingId.value = response.data.id;
  })
  .catch(error => {
    console.error('평가 등록 에러:', error);
  });
};

const deleteRating = () => {
  const movieId = route.params.movieId;
  axios.delete(
    `${store.API_URL}/api/v1/movies/${movieId}/rating/${ratingId.value}/`,
    {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    }
  )
  .then(response => {
    console.log('평가 삭제 완료:', response.data);
    ratinggg.value = '';
    ratingId.value = null;
  })
  .catch(error => {
    console.error('평가 삭제 에러:', error);
  });
};

onMounted(() => {
  fetchRating(route.params.movieId);
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.rating-container {
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: rgb(255, 253, 239);
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  border-radius: 8px;
}

/* 제목 스타일 */
.rating-title {
  color: #4A90E2;
  font-size: 1.8em;
  margin-bottom: 20px;
}

/* 평점 표시 스타일 */
.rating-display {
  color: #007bff;
  font-size: 1.2em;
  margin-bottom: 20px;
}

/* 폼 스타일 */
.rating-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: medium;
}

/* 레이블 스타일 */
.rating-label {
  margin-bottom: 10px;
  font-size: 1.2em;
  color: #555;
}

/* 입력 필드 스타일 */
.rating-input {
  width: 50%;
  padding: 10px;
  font-size: 1em;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

/* 버튼 스타일 */
.rating-button {
  width: 50%;
  padding: 10px;
  font-size: 1em;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.rating-button:hover {
  background-color: #0056b3;
}

/* 삭제 버튼 스타일 */
.rating-delete-button {
  width: 50%;
  padding: 10px;
  font-size: 1em;
  color: #fff;
  background-color: #b5b9c6;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.rating-delete-button:hover {
  background-color: #7791e8;
}
</style>
