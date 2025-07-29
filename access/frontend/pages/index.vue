<template>
  <div>
    <h1 class="main-title"> 📰 NewsBias: Bias Tracking and Emerging Topics across News Outlets</h1>
      
    

    <table>
      <tr>  
        <td class="col-3 align-top">
          <NewsSourceInfo />
        </td>
        <td class="col-6">
          <KnowledgeGraph />
        </td>
        <td class="col-3 align-top" style>
          <Documentation />
        </td>
      </tr>
      
    </table>

    <table>
      <tr>
        
        <td class="col-12 align-middle">
          <KeywordFinder />
        </td>
        
      </tr>
    </table>


   
  </div>
</template>


<script setup>
import { ref } from 'vue'

// The KeywordFinder component will be auto-imported by Nuxt

const generateResponse = () => {
  console.log('Generating response...')
}
</script>

<style scoped>
.main-title {
  color: #8B5FBF;
  font-size: 28px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 30px;
  padding-bottom: 15px;
  margin:20px;
  border-bottom: 3px solid #8B5FBF;
  
  padding-left: 100px;
  float: left;
  width: 100%;
  
}

td {
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
}





</style> 