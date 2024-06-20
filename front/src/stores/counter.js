import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () =>{
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  // 사용자 정보를 저장하기 위한 ref 생성
  // const userId = ref(null)
  // const nickname = ref(null)
  const movie = ref([])
  const movieList = ref([])
  const router = useRouter()
  const route = useRoute()
  const currentUser = ref({ userId: null, nickname: null })
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  
  // 회원가입
  const signUp = function (payload) {
    const { username, password1, password2, nickname } = payload
    
    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/registration/`,
      data: { username, password1, password2, nickname }
    })
      .then((response) => {
        console.log('회원가입 성공!')
        // 회원가입 성공 후 자동으로 로그인까지 진행
        const password = password1
        login({ username, password })
      })
      .catch((error) => {
        console.log(error)
      })
  }


  // 로그인
  const login = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/login/`,
      data: { username, password }
    })
      .then((res) => {
        token.value = res.data.key
        localStorage.setItem('token', res.data.key) // 로컬 스토리지에 토큰 저장
        console.log('로그인이 완료되었습니다.')
        // console.log(res.data)
        token.value = res.data.key
        getUserObj()
        router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.log(err)
        window.alert('아이디 또는 비밀번호가 올바르지 않습니다.')
      })
  }

  const logout = function () {
    axios({
      method: 'post',
      url: `${API_URL}/dj-rest-auth/logout/`,
    })
      .then(() => {
        console.log('로그아웃 성공!')
        // 토큰 삭제 또는 초기화
        localStorage.removeItem('token')
        token.value = null // 토큰 값을 null로 설정하여 로그아웃 상태를 명확히 함
        router.push({ name: 'LoginView' })
      })
      .catch((error) => {
        console.log(error);
      })
  }  
  
  // 현재 로그인한 유저 정보를 가져오는 함수
  const getUserObj = async function () {
    try {
      const response = await axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/accounts/get_user_obj/`,
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
      console.log('사용자 정보가 저장되었습니다.')
      // 사용자 정보를 currentUser에 저장
      currentUser.value.userId = response.data.id
      currentUser.value.nickname = response.data.nickname
      // console.log(currentUser.value.userId)
      // console.log(currentUser.value.nickname)
    } catch (error) {
      console.log(error)
    }
  }

  const getMovieDetail = function (movieId) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/${movieId}/detail/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
      .then(res => {
        movie.value = res.data
        // console.log(movie.value)
      })
      .catch(err => console.log(err))
  }

  const deleteMovie = async (categoryId, movieId) => {
    try {
      await axios({
        method: 'delete',
        url: `${store.API_URL}/api/v1/categories/${categoryId}/update/${movieId}`,
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
      const index = movieList.value.findIndex(m => m.id === movieId)
      if (index !== -1) {
        movieList.value.splice(index, 1)
      }
      await getUserProfile()
    } catch (err) {
      console.error('Error deleting note:', err)
    }
  }
  return { token, movie, API_URL, route, router, isLogin, currentUser, movieList, signUp, login, logout, getMovieDetail, getUserObj, deleteMovie }
}, { persist: true })