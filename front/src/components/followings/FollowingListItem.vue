<template>
  <div class="following-item">
    <RouterLink :to="{ name: 'ProfileView', params: { userId: following.id }}" class="link">
      <div class="following-item-content">
        <img
          :src="`https://api.dicebear.com/8.x/adventurer-neutral/svg?seed=${following.nickname}&radius=50`"
          alt="avatar"
          class="avatar"
        />
        <p class="nickname">{{ following.nickname }}</p>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
  following: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.following-item {
  display: flex;
  align-items: center;
}

.following-item-content {
  display: flex;
  align-items: center;
  gap: 20px; /* 이미지와 닉네임 간의 간격 */
}

.avatar {
  width: 40px; /* 이미지 크기 */
  height: 40px; /* 이미지 크기 */
  border-radius: 50%; /* 원형 이미지 */
  transition: transform 0.5s ease; /* 호버 시 크기 변화 애니메이션 */
}

.link {
  text-decoration: none; /* 링크의 기본 밑줄 제거 */
}

.nickname {
  font-size: 14px; /* 글자 크기 */
  color: #5197e2; /* 폰트 컬러 설정 */
  text-decoration: none; /* 기본 밑줄 제거 */
  transition: transform 0.5s ease; /* 호버 시 크기 변화 애니메이션 */
}

.following-item:hover .avatar,
.following-item:hover .nickname {
  transform: scale(1.4); /* 호버 시 텍스트와 이미지 크기 확대 */
}
</style>
