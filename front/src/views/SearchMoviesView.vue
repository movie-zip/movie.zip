<template>
  <div class="movie-search-container">
    <div class="search-bar">
      <input v-model="query" @keyup.enter="searchMovies" placeholder="Search movies..." />
      <button @click="searchMovies" class="search-button">Search</button>
    </div>
    <div v-if="movies.length" class="movie-list">
      <div v-for="movie in movies" :key="movie.id" class="movie-item">
        <RouterLink :to="{name:'MovieDetailView', params:{movieId:movie.id}}" class="link">
          <div class="movie-card">
            <img :src="movie.poster" alt="Movie Poster" v-if="movie.poster" />
            <h3>{{ movie.title }}</h3>
          </div>
        </RouterLink>
      </div>
    </div>
    <p v-else class="no-results">No search results found.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter.js';
import MovieDetailView from './MovieDetailView.vue';

const store = useCounterStore();
const query = ref('');
const movies = ref([]);

const searchMovies = async () => {
  if (!query.value.trim()) {
    alert('Please enter a search query.');
    return;
  }
  try {
    const response = await axios.get(`${store.API_URL}/api/v1/movies/search/`, {
      params: {
        query: query.value
      }
    });
    const results = response.data.results || [];
    movies.value = results.map(movie => ({
      ...movie,
      poster: movie.poster ? `https://image.tmdb.org/t/p/w500${movie.poster}` : null,
    }));
  } catch (error) {
    console.error('Error searching for movies:', error);
    alert('An error occurred while searching for movies.');
  }
};
</script>

<style scoped>
.movie-search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar {
  display: flex;
  margin-bottom: 20px;
}

.search-bar input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px 0 0 4px;
}

.search-bar .search-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.search-bar .search-button:hover {
  background-color: #0056b3;
}

.link {
  text-decoration: none;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-item {
  /* flex: 1 1 calc(33.333% - 20px); */
  box-sizing: border-box;
}

.movie-card {
  border-radius: 8px;
  width:250px;
  height:450px;
  text-align: center;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-card img {
  width: 100%;
  height: 350px;
  border-radius: 8px;
}

.movie-card h3 {
  margin: 10px 0;
  font-size: 18px;
}

.movie-card p {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #777;
}

.no-results {
  text-align: center;
  font-size: 18px;
  color: #777;
}


</style>
