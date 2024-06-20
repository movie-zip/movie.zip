<template>
  <div class="following-note-list-container">
    <h2 class="subscription-title">타임라인</h2>
    <FollowingNoteListItem
      v-for="note in notes"
      :key="note.id"
      :note="note"
    />
  </div>
</template>
  
<script setup>
import { useCounterStore } from '@/stores/counter.js'
import FollowingNoteListItem from '@/components/notes/FollowingNoteListItem.vue'
import { defineProps } from 'vue';

const store = useCounterStore()

defineProps({
  notes: Array
})
</script>

<style scoped>
.following-note-list-container {
  margin-top: 40px; /* 내브바와의 간격 */
  display: flex;
  flex-direction: column;
  gap: 40px; /* 게시글 사이 간격 */
}
.subscription-title {
  text-align: center; /* 텍스트 중앙 정렬 */
  color: #5197e2; /* 글자색 설정 */
}
</style>