<template>
  <div class="modal-overlay" @click="close">
    <div class="modal-container" @click.stop>
      <div class="modal-content">
        <slot></slot>
      </div>
      <button class="close-button" @click="close">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background: white;
  width: 60%; /* 모달의 너비를 화면의 60%로 설정 */
  width: 640px; /* 최대 너비 설정 */
  height: 400px; /* 최소 높이 설정 */
  border-radius: 10px;
  padding: 40px; /* 내부 패딩을 넉넉하게 설정 */
  display: flex;
  flex-direction: column; /* 버튼을 아래에 위치시키기 위해 flex-direction 설정 */
  align-items: center; /* 내용을 중앙 정렬 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 모달에 그림자 추가 */
}

.modal-content {
  flex-grow: 1; /* 콘텐츠 영역을 모달 컨테이너 내에서 가능한 많이 차지하도록 설정 */
  width: 100%; /* 콘텐츠 너비를 모달 컨테이너와 같게 설정 */
  margin-bottom: 20px; /* 콘텐츠와 닫기 버튼 사이의 간격 설정 */
}

.close-button {
  padding: 10px 20px; /* 버튼 패딩 설정 */
  font-size: 16px; /* 글자 크기 설정 */
  border: none; /* 테두리 제거 */
  background-color: #f44336; /* 배경색 설정 */
  color: white; /* 글자색 설정 */
  border-radius: 5px; /* 버튼 모서리 둥글게 설정 */
  cursor: pointer; /* 마우스 오버 시 커서 변경 */
}

.close-button:hover {
  background-color: #d32f2f; /* 마우스 오버 시 배경색 변경 */
}
</style>
