<template>
  <div class="container">
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <div class="input-group">
        <label for="username">아이디 : </label>
        <input type="text" v-model.trim="username" id="username">
      </div>
      <div class="input-group">
        <label for="password1">비밀번호 : </label>
        <input type="password" v-model.trim="password1" id="password1">
      </div>
      <div class="input-group">
        <label for="password2">비밀번호 확인 : </label>
        <input type="password" v-model.trim="password2" id="password2">
      </div>
      <div class="input-group">
        <label for="nickname">닉네임 : </label>
        <input type="text" v-model.trim="nickname" id="nickname">
      </div>
      <input type="submit" value="회원가입" class="submit-button">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value
  }
  store.signUp(payload)
}

</script>

<style scoped>
.container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 10px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  padding: 15px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

.submit-button:hover {
  opacity: 1;
}
</style>