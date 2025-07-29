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

    <KeywordFinder />
  </div>
</template>

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
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  padding-left: 100px;
  float: left;
  width: 100%;
  
}

td {
  padding: 10px;
}
</style>