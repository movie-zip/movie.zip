<template>
  <div class="note-container">
    <p v-if="note">{{ note.content }}</p>
    <p v-else>Loading note...</p>
    <!-- Edit and Delete buttons -->
    <div v-if="isMyNote" class="button-container">
      <button class="edit-button" @click="editNote">수정</button>
      <button class="delete-button" @click="deleteNote">삭제</button>
    </div>
    <!-- Note editing form -->
    <div v-if="isEditing" class="edit-form">
      <textarea v-model="editedContent" class="edit-textarea"></textarea>
      <button class="save-button" @click="saveNote">저장</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const note = ref(null)
const isEditing = ref(false)
const editedContent = ref('')

const noteUserId = ref(null)  // 노트 작성자의 id
const userId = computed(() => store.currentUser.userId)  // 내 id
const isMyNote = computed(() =>  Number(userId.value) === Number(noteUserId.value))

const props = defineProps({
  note:Object
})

onMounted(async () => {
  try {
    const res = await axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/notes/${route.params.noteId}/detail/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    note.value = res.data  // 가져온 노트 데이터를 할당
    noteUserId.value = res.data.user  // 노트 작성자의 ID를 업데이트
    console.log(res.data)
  } catch (err) {
    console.error('Error fetching note details:', err)
    note.value = { content: 'Error occurred while loading the note.' }
  }
})

const editNote = () => {
  isEditing.value = true
  editedContent.value = note.value.content
}

const saveNote = async () => {
  try {
    const res = await axios({
      method: 'put',
      url: `${store.API_URL}/api/v1/notes/${route.params.noteId}/detail/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      },
      data: {
        content: editedContent.value
      }
    })
    note.value = res.data
    isEditing.value = false
  } catch (err) {
    console.error('Error saving note:', err)
  }
}

const deleteNote = async () => {
  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/notes/${route.params.noteId}/detail/`,
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    router.go(-1)  // 이전 페이지로 이동
  } catch (err) {
    console.error('Error deleting note:', err)
  }
}
</script>

<style scoped>
.note-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  max-width: 600px;
  margin: 50px auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h2 {
  margin-bottom: 20px;
}

p {
  margin: 10px 0;
}

.button-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.edit-button, .delete-button, .save-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-button {
  background-color: #abb3bc;
  color: white;
}

.edit-button:hover {
  background-color: #45a049;
}

.delete-button {
  background-color: #7d8286;
  color: white;
}

.delete-button:hover {
  background-color: #d32f2f;
}

.save-button {
  background-color: #8dcbfd;
  color: white;
}

.save-button:hover {
  background-color: #1976d2;
}

.edit-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.edit-textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: none;
}
</style>
