<template>
  <div class="following-list-container">
    <h2 class="subscription-title">구독</h2>
    <FollowingListItem 
      v-for="following in followings.followings" 
      :key="following.id" 
      :following="following" />
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import FollowingListItem from "@/components/followings/FollowingListItem.vue";

const props = defineProps({
  followings: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.following-list-container {
  margin-top: 40px; /* 내브바와의 간격 */
  display: flex;
  flex-direction: column;
  gap: 40px; /* 팔로잉 항목 간의 간격 */
}
.subscription-title {
  text-align: center; /* 텍스트 중앙 정렬 */
  color: #5197e2; /* 글자색 설정 */
}
</style>
