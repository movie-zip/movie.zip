<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="navbar">
        <RouterLink class="nav-link shared-link-button" :to="{ name: 'HomeView' }">
          홈
        </RouterLink>
        
        <!-- 로그인 상태일 때 프로필과 로그아웃 링크를 보여줍니다. -->
        <RouterLink v-if="isLogin" class="nav-link shared-link-button" :to="{ name: 'ProfileView', params: { userId: `${userId}` } }">
          프로필
        </RouterLink>
        
        <RouterLink class="nav-link shared-link-button" :to="{ name : 'SearchMoviesView' }">
          검색
        </RouterLink> 
        
        <button v-if="isLogin" class="logout-button shared-link-button" @click="store.logout">
          로그아웃
        </button>
        
        <!-- 로그인 상태가 아닐 때 로그인 버튼을 보여줍니다. -->
        <RouterLink v-else class="nav-link shared-link-button" :to="{ name: 'LoginView' }">
          로그인
        </RouterLink>
      </nav>
    </header>
    <main class="app-content">
      <Suspense>
        <template #default>
          <RouterView />
        </template>
        <template #fallback>
          <div>로딩 중...</div>
        </template>
      </Suspense>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, Suspense } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
// 스토어의 isLogin 계산된 속성을 사용하여 로그인 상태를 확인합니다.
const isLogin = computed(() => store.isLogin)
const userId = computed(() => store.currentUser.userId)

onMounted(async () => {
  await store.getUserObj()
})
</script>

<style scoped>
@font-face {
  font-family: 'wavefont';
  src: url(assets/fonts/WavvePADO-Regular.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet1';
  src: url(assets/fonts/SUITE-Heavy.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet2';
  src: url(assets/fonts/SUITE-ExtraBold.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet3';
  src: url(assets/fonts/SUITE-Bold.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet4';
  src: url(assets/fonts/SUITE-SemiBold.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet5';
  src: url(assets/fonts/SUITE-Medium.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet6';
  src: url(assets/fonts/SUITE-Regular.ttf) format('truetype');
}
@font-face {
  font-family: 'sweet7';
  src: url(assets/fonts/SUITE-Light.ttf) format('truetype');
}

.app-container {
  font-family: 'sweet6', sans-serif;
}

.app-header {
  background-color: rgb(202, 244, 255); /* 밝은 파란색 */
  padding: 10px 20px; /* 상하 여백을 줄임 */
  position: fixed; /* 헤더를 고정시킴 */
  top: 0; /* 화면 상단에 위치 */
  width: 100%; /* 전체 너비 */
  z-index: 1000; /* 다른 콘텐츠보다 위에 표시 */
}

.navbar {
  display: flex;
  justify-content: center;
  list-style: none;
  align-items: center; /* 항목들이 중앙에서 정렬되도록 함 */
}

.shared-link-button {
  color: #5197e2; /* 글자 색상 */
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px;
  cursor: pointer;
  border-radius: 20px; /* 버튼 모서리를 둥글게 */
  transition: background-color 0.3s, color 1s; /* 부드러운 색상 전환 효과 */
  font-family: 'sweet6';
  font-size: 16px; /* 글자 크기 설정 */
}

.logout-button {
  background-color: rgb(202, 244, 255); /* 네비게이션 바 배경색과 동일 */
  border: none; /* 테두리 제거 */
  margin-left: auto; /* 오른쪽 정렬을 위해 자동 마진 적용 */
  margin-right: 25px;
}

.shared-link-button:hover, .logout-button:hover {
  background-color: #5197e2; /* 호버 시 배경색 */
  color: rgb(202, 244, 255); /* 호버 시 글자 색상 */
}

.app-content {
  padding-top: 60px; /* 헤더 높이만큼 여백을 추가하여 컨텐츠가 네비게이션 바 뒤에 숨지 않도록 함 */
  padding-left: 0px;
}
</style>
