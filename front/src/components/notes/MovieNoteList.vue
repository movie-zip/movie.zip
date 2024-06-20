<template>
    <div>
        <MovieNoteListItem 
        v-for="note in notesss"
        :key="note.id"
        :note="note"/>
    </div>
</template>

<script setup>
import MovieNoteListItem from '@/components/notes/MovieNoteListItem.vue'
const props = defineProps({
  notesss:Array
})
</script>

<style scoped>

</style>