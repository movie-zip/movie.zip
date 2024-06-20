<template>
  <div>
    <h2>{{ nickname }}님이 작성한 노트</h2>
    <div v-if="notes.length">
      <Carousel :items-to-show="3" :wrap-around="true">
        <Slide v-for="note in notes" :key="note.id">
          <NoteListItem :note="note" />
        </Slide>
        <template #addons>
          <Navigation />
        </template>
      </Carousel>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import NoteListItem from '@/components/notes/NoteListItem.vue'
import 'vue3-carousel/dist/carousel.css'
import { Carousel, Slide, Navigation } from 'vue3-carousel'

const notes = ref([])
const store = useCounterStore()
const route = useRoute()
const nickname = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/notes/${route.params.userId}/list/`,
  })
    .then((response) => {
      notes.value = response.data
      nickname.value = response.data[0].user.nickname
    })
    .catch((error) => {
      console.log(error)
    })
})
</script>

<style scoped>
div {
  padding: 20px;
  background-color: rgb(255, 253, 239);
  border-radius: 8px;
  align-content: center;
  align-items: center;
}

h2 {
  font-family: 'sweet6';
  color: #5197e2;
  margin-bottom: 16px;
  font-size: 24px;
  text-align: center;
}


.note-list-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.link {
  text-decoration: none;
}

.note-list-item h4 {
  margin: 0;
  text-align: center;
}

.note-list-item img {
  width: 80px;
  height: auto;
  border-radius: 4px;
  margin-bottom: 16px;
}

</style>
