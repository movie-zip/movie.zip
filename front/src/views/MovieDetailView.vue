<template>
  <div class="container">
    <!-- <h1 class="title">영화 상세정보 페이지 입니다.</h1> -->
    <MovieInfo :movie="movie" />
    <form @submit.prevent="addMovieToCategory" class="form-container">
      <select name="category" v-model="selectedCategory" class="select-box">
        <option value="" disabled selected>카테고리를 선택하세요</option>
        <option v-if="categories[0]" :value="categories[0].id">나의 TOP 5 영화</option>
        <option v-if="categories[1]" :value="categories[1].id">내가 본 영화</option>
        <option v-if="categories[2]" :value="categories[2].id">내가 볼 영화</option>
        <template v-for="(category, index) in categories.slice(3)" :key="category.id">
          <option :value="category.id">{{ category.name }}</option>
        </template>
      </select>
      <input type="submit" value="추가" class="submit-button" />
    </form>
    <MovieRank />
    
    <div class="button-container">
      <button @click="showModal = true">작성하기</button>
    </div>
    <Modal v-if="showModal" @close="handleClose">
      <h2>노트 작성하기</h2>
      <form @submit.prevent="submitNote">
        <textarea id="content" v-model="content" required></textarea>
        <button type="submit">작성하기</button>
      </form>
    </Modal>
     <h2 class="title">내가 작성한 노트</h2>
    <MovieMyNoteList :notes="notes" />
     <h2 class="title">다른 사용자들이 작성한 노트</h2>
    <MovieNoteList :notesss="notesss" />
  </div>
</template>


<script setup>
import axios from 'axios';
import { onMounted, ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import MovieInfo from '@/components/movies/MovieInfo.vue';
import MovieMyNoteList from '@/components/notes/MovieMyNoteList.vue';
import MovieNoteList from '@/components/notes/MovieNoteList.vue';
import MovieRank from '@/components/movies/MovieRank.vue';
import Modal from '@/components/Modal.vue';

const store = useCounterStore();
const router = useRouter();
const route = useRoute();
const movie = ref([]);
const notes = ref([]);
const notesss = ref([]);
const categories = ref([]);
// const userId = ref(null);/
const selectedCategory = ref(''); // 초기값을 null로 변경
const isModalVisible = ref(false);
const content = ref('')

const fetchMovieDetails = async (movieId) => {
  try {
    const response = await axios.get(`${store.API_URL}/api/v1/movies/${movieId}/detail/`);
    movie.value = response.data;
  } catch (error) {
    console.log(error);
  }
};
const userId = computed(() => store.currentUser.userId)

const fetchUserNotes = async (movieId) => {
  try {
    const response = await axios.get(`${store.API_URL}/api/v1/notes/${userId.value}/list/${movieId}/`);
    notes.value = response.data;
  } catch (error) {
    console.log(error);
  }
};

const fetchOtherNotes = async (movieId) => {
  try {
    const response = await axios.get(`${store.API_URL}/api/v1/notes/other/list/${movieId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    notesss.value = response.data;
  } catch (error) {
    console.log(error);
  }
};

// 유저 정보 가져와서 유저가 가진 카테고리 목록 뽑아내기
const getUserProfile = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/profile/${userId.value}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    // console.log(response.data.my_categories);
    categories.value = response.data.my_categories;
  } catch (error) {
    console.log(error);
  }
};

// 특정 카테고리에 영화 추가
const addMovieToCategory = async () => {
  const movieId = route.params.movieId;
  const categoryId = selectedCategory.value; // 선택된 카테고리 ID를 사용

  try {
    const response = await axios.post(
      `${store.API_URL}/api/v1/categories/${categoryId}/update/${movieId}/`,
      {
        movie_id: movieId,
        category_name: categories.value.find(category => category.id === categoryId)?.name
      },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      }
    );
    alert(response.data.message);
    console.log('영화가 카테고리에 추가되었습니다:', response.data);

    // 영화를 카테고리에 추가한 후에 selectedCategory 값을 초기화
    selectedCategory.value = '';
  } catch (error) {
    console.error('영화 추가 중 에러 발생:', error);
    if (error.response && error.response.data && error.response.data.error) {
      alert(error.response.data.error);
    }
  }
};

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
    notes.value.push(response.data); // 작성된 노트를 notes 배열에 추가
    content.value = ''; // 내용을 초기화
    handleClose(); // 모달을 닫습니다.
    router.push({ name: 'MovieDetailView', params: { movieId: movieId } });
  })
  .catch(error => {
    console.error('노트 작성 에러:', error);
  });
};

const showModal = ref(false);

const close = () => {
  isModalVisible.value = false;
};

const handleClose = () => {
  showModal.value = false;
};

onMounted(async () => {
  const movieId = route.params.movieId;
  await store.getUserObj()
  await fetchMovieDetails(movieId);
  await fetchUserNotes(movieId);
  await fetchOtherNotes(movieId);
  userId.value = store.currentUser.userId;
  if (userId.value) {
    await getUserProfile();
  } else {
    console.log('User ID is null');
  }
});
console.log(`카테고리 : ${categories.value}`);

</script>

<style scoped>
/* 페이지의 전체적인 레이아웃을 설정합니다 */
.container {
  padding: 20px;
  background-color: rgb(255, 253, 239); /* 배경색 추가 */
  max-width: 800px; /* 최대 너비 설정 */
  margin: 0 auto; /* 좌우 가운데 정렬 */
  align-items: center;
  align-content: center;
  font-family: 'sweet6';
}

/* 제목 스타일링 */
.title {
  color: #4A90E2;
  text-align: center;
  font-size: 2em;
  font-weight: 900;
  margin-bottom: 10px;
}

/* 구분선 스타일링 */
.divider {
  border: 0;
  height: 1px;
  background: #eee;
  margin: 20px 0;
}

/* 선택 박스와 제출 버튼 컨테이너 스타일링 */
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

/* 선택 박스 스타일링 */
.select-box {
  width: 80%; /* 너비를 조정하여 가운데 정렬 */
  padding: 10px;
  font-size: 1em;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

/* 제출 버튼 스타일링 */
.submit-button {
  width: 80%; /* 너비를 조정하여 가운데 정렬 */
  padding: 10px;
  font-size: 1em;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s; /* 배경색 변화 애니메이션 추가 */
}

.submit-button:hover {
  background-color: #0056b3;
}

/* 노트 작성 버튼 스타일링 */
.note-button {
  width: 80%; /* 너비를 조정하여 가운데 정렬 */
  padding: 10px;
  font-size: 1em;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s; /* 배경색 변화 애니메이션 추가 */
  margin: 20px 0;
}

.note-button:hover {
  background-color: #0056b3;
}

button {
  background-color: #4CAF50; /* 배경 색상 */
  border: none; /* 테두리 제거 */
  color: white; /* 텍스트 색상 */
  padding: 15px 32px; /* 패딩 */
  text-align: center; /* 텍스트 정렬 */
  text-decoration: none; /* 텍스트 데코레이션 제거 */
  display: inline-block; /* 인라인 블록 요소로 표시 */
  font-size: 16px; /* 폰트 크기 */
  margin: 4px 2px; /* 마진 */
  cursor: pointer; /* 커서 모양 변경 */
  border-radius: 12px; /* 테두리 반경 */
  transition: background-color 0.3s; /* 배경색 전환 효과 */
}

/* 개별 컴포넌트의 컨테이너 스타일링 */
.movie-info, .movie-my-note-list, .movie-note-list, .movie-rank {
  margin: 20px 0;
}

textarea {
  width: 70%; /* 너비를 조정하여 가운데 정렬 */
  height: 200px;
  padding: 10px;
  font-size: 1em;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

.button-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

button {
  background-color: #007bff; 
  border: none; 
  color: white; 
  padding: 15px 15px; 
  text-align: center; 
  text-decoration: none; 
  display: inline-block; 
  font-size: 14px; 
  margin: 4px 2px; 
  cursor: pointer; 
  border-radius: 8px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
