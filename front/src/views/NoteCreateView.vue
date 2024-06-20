<template>
    <div>
      <button @click="showModal = true" class="note-button">노트 작성</button>
      <Modal v-if="showModal" @close="handleClose" />
        <h2>노트 작성하기</h2>
        <form @submit.prevent="submitNote">
          <label for="content">내용:</label>
          <textarea id="content" v-model="content" required></textarea>
          <button type="submit">작성하기</button>
        </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useCounterStore } from '@/stores/counter';
  import axios from 'axios';
  import Modal from '@/components/Modal.vue'; // 모달 컴포넌트 경로를 정확히 입력하세요.
  
  const store = useCounterStore();
  const isModalVisible = ref(false);
  const content = ref('');
  
  const showModal = () => {
    isModalVisible.value = true;
  };
  
  const hideModal = () => {
    isModalVisible.value = false;
  };
  
  const route = useRoute();
  const router = useRouter();
  
  const submitNote = () => {
    const movieId = route.params.movieId;
    const requestData = {
      content: content.value
    };
  
    axios.post(
      `${store.API_URL}/api/v1/notes/${movieId}/`,
      requestData,
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        }
      }
    )
    .then(response => {
      console.log('노트 작성 완료:', response.data);
      hideModal();
      router.push({ name: 'MovieDetailView', params: { movieId: movieId } });
    })
    .catch(error => {
      console.error('노트 작성 에러:', error);
    });
  };
  
  </script>
  
  <style scoped>
  .note-button {
    /* 스타일 추가 */
  }
  </style>
  