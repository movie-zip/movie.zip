import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faPencilAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import App from './App.vue'
import router from './router'

library.add(faTrash, faPencilAlt)

const app = createApp(App)  // 'app' 변수를 먼저 초기화합니다.
app.component('font-awesome-icon', FontAwesomeIcon)  // 이제 'app' 변수를 사용할 수 있습니다.

const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.mount('#app')