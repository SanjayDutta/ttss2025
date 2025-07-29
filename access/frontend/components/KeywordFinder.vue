<template>
  <div class="keyword-finder">
    <div class="search-container">
      <h2>Keyword Finder</h2>
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @keyup.enter="searchKeywords"
          placeholder="Enter your search query..."
          class="search-input"
        />
        <button @click="searchKeywords" class="search-btn">Search</button>
      </div>
      
      <div v-if="loading" class="loading">
        Searching for keywords...
      </div>
      
      
      
      <div v-if="keywordArray.length > 0" class="keyword-array-display">
        <strong>Split Keywords:</strong>
        <ul>
          <li v-for="(kw, idx) in keywordArray" :key="idx">{{ kw }}</li>
        </ul>
      </div>
      
      <div v-if="htmlResponse" class="html-response">
        <h3>Articles Found:</h3>
        <div v-html="htmlResponse" class="response-content"></div>
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchQuery = ref('')
const keywords = ref([])
const loading = ref(false)
const error = ref('')
const keywordArray = ref([])
const htmlResponse = ref('')

const searchKeywords = async () => {
  if (!searchQuery.value.trim()) {
    error.value = 'Please enter a search query'
    return
  }
  
  // Split the search query by commas and trim whitespace
  keywordArray.value = searchQuery.value.split(',').map(k => k.trim()).filter(k => k.length > 0)

  loading.value = true
  error.value = ''
  keywords.value = []
  htmlResponse.value = '' // Clear previous HTML response
  
  try {
    // Make axios call to fetch articles based on keywords
    const response = await $fetch('http://127.0.0.1:8001/fetch_articles_keywords', {
      method: 'POST',
      body: {
        keywords: keywordArray.value
      }
    })
    
    console.log('API Response:', response)
    
    // Store the HTML response
    htmlResponse.value = response
    
    // Handle the response - you can modify this based on your API response structure
    if (response && response.articles) {
      keywords.value = response.articles
    } else {
      keywords.value = response || []
    }
    
  } catch (err) {
    error.value = 'Failed to fetch articles. Please try again.'
    console.error('API Error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.keyword-finder {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  float: left;
  padding: 20px;
  margin-right: 350px;
}

.search-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-right: 150px;
}

h2 {
  margin: 0 0 20px 0;
  color: #333;
  text-align: center;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  margin-right: 150px;
}

.search-input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #0074D9;
}

.search-btn {
  padding: 12px 24px;
  background: #772cd3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

.search-btn:hover {
  background: #490282;
}

.loading {
  text-align: center;
  color: #666;
  font-style: italic;
  margin: 20px 0;
}

.results {
  margin-top: 20px;
}

.results h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.keyword-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.keyword-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #0074D9;
}

.keyword-text {
  font-weight: 500;
  color: #333;
}

.keyword-score {
  background: #0074D9;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.keyword-array-display {
  margin-top: 16px;
  background: #f1f8e9;
  border: 1px solid #c5e1a5;
  border-radius: 6px;
  padding: 10px;
  color: #33691e;
}

.html-response {
  margin-top: 20px; 
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  min-width: 800px;
}

.html-response h3 {
  margin: 0 0 15px 0;
  color: #333;
  border-bottom: 2px solid #0074D9;
  padding-bottom: 8px;
}

.response-content {
  max-height: 500px;
  overflow-y: auto;
  line-height: 1.6;
}

.error {
  color: #dc3545;
  text-align: center;
  margin: 20px 0;
  padding: 10px;
  background: #f8d7da;
  border-radius: 6px;
  border: 1px solid #f5c6cb;
}

.search-query {
  color: #0074D9;
  font-weight: bold;
  background: #e3f2fd;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #bbdefb;
}
</style> 