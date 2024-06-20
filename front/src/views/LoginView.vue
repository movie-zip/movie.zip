<template>
  <div>
      <h1>로그인</h1>
      <form @submit.prevent="login">
        <label for="username"> 아이디 </label>
        <input type="text" id="username" v-model.trim="username"><br>
        
        <label for="password"> 비밀번호 </label>
        <input type="password" id="password" v-model.trim="password"><br>

        <input type="submit" value="로그인"> <br/>
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>

      </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore();

const username = ref(null);
const password = ref(null);

const login = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    store.login(payload)
  }

</script>

<style scoped>
div {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  /* border: 1px solid #ccc; */
  border-radius: 5px;
  /* background-color: #f9f9f9; */
}

h1 {
  color: #333;
  text-align: center;
}

label {
  margin-top: 10px;
  display: block;
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  width: 95.5%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #4cae4c;
  transform: scale(1.02)
}

a {
  display: block;
  margin-top: 20px;
  text-align: center;
  color: #337ab7;
  text-decoration: none;
  transition: transform 0.3s ease;
}

a:hover {
  transform: scale(1.1)
}
</style>