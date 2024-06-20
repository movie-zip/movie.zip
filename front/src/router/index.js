import { createRouter, createWebHistory } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import HomeView from '@/views/HomeView.vue'
import ProfileView from '@/views/ProfileView.vue'
import MyMovieList from '@/components/profile/MyMovieList.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import NoteDetailView from '@/views/NoteDetailView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import UserUpdateView from '@/views/UserUpdateView.vue'
import FollowingView from '@/views/FollowingView.vue'
import CustomCategoryView from '@/views/CustomCategoryView.vue'
import WatchedMovieView from '@/components/profile/WatchedMovieView.vue'
import ToWatchMovieView from '@/components/profile/ToWatchMovieView.vue'
import NotesView from '@/components/profile/NotesView.vue'
import NoteCreateView from '@/views/NoteCreateView.vue'
import SearchMoviesView from '@/views/SearchMoviesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/signUp',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/',
      name: 'HomeView',
      component: HomeView
    },
    {
      path: '/profile/:userId',
      name: 'ProfileView',
      component: ProfileView,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'myMovies',
          component: MyMovieList
        },
        {
          path: 'notes',
          name: 'notes',  // Add this line
          component: NotesView
        },
        {
          path: 'watched',
          name: 'watched',
          component: WatchedMovieView
        },
        {
          path: 'towatch',
          name: 'towatch',
          component: ToWatchMovieView
        },
        {
          path: 'category/:categoryId',
          name: 'category',
          component: CustomCategoryView
        }
      ]
    },
    {
      // path: '/movie/12',
      path: '/movie/:movieId',
      name: 'MovieDetailView',
      component: MovieDetailView
    },
    {
      path: '/note/:noteId',
      name: 'NoteDetailView',
      component: NoteDetailView
    },
    {
      path: '/update-user',
      name: 'UserUpdateView',
      component: UserUpdateView
    },
    {
      path: '/following-list/:userId',
      name: 'FollowingView',
      component: FollowingView
    },
    {
      path: '/category/:categoryId',
      name: 'CustomCategoryView',
      component: CustomCategoryView
    },
    {
      path: '/watched-movies',
      name: 'WatchedMovieView',
      component: WatchedMovieView
    },
    {
      path: '/to-watch-movies',
      name: 'ToWatchMovieView',
      component: ToWatchMovieView
    },
    {
      path: '/notes/:userId',
      name: 'NotesView',
      component: NotesView
    },
    {
      path: '/notes/create/:movieId',
      name: 'NoteCreateView',
      component: NoteCreateView,
      meta: { modal:true}
    },
    {
      path: '/search',
      name: 'SearchMoviesView',
      component: SearchMoviesView
    },
  ]
  
})

router.beforeEach((to, from, next) => {
  // 로그인 상태 확인. 예를 들어 localStorage에서 토큰을 확인하는 방식.
  // 실제 로그인 상태 확인 로직은 프로젝트의 인증 구조에 맞게 조정해야 합니다.
  const isLogin = localStorage.getItem('token');

  if (!isLogin && to.name !== 'LoginView' && to.name !== 'SignUpView') {
    // 로그인 상태가 아니고, 현재 경로가 로그인 페이지가 아닌 경우 로그인 페이지로 리디렉트합니다.
    next({ name: 'LoginView' });
  } else {
    // 로그인 상태이거나 로그인 페이지인 경우, 원하는 경로로 진행합니다.
    next();
  }
});

export default router
