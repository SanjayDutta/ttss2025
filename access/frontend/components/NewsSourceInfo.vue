<template>
  <div class="news-source-info">
   <table>
    <tr style="background-image: linear-gradient(to right, #080112, #23064f); color: white;">
        <th>News Outlet</th>
        <th>Popular Keywords</th>
        <th>Bias</th>
    </tr>
    <tr style="background-image: linear-gradient(to right, purple, #772cd3); color: white;">
      <td>
        Breitbart News Network
      </td>
      <td>
        <i style="font-size:10px;">US Elections, Politics, DEI, Trump, Woke</i>
       </td>
      <td>
        Conservative
      </td>
    </tr>
    <tr style="background-image: linear-gradient(to right, #772cd3, purple); color: white;">
        <td>The Guardian</td>
        <td style="font-size:10px;"><i>UK Politics, Brexit, Middle East, Climate Crisis</i></td>
        <td>Left-wing</td>
    </tr>
   </table>

   <br>
   <table style="background-image: linear-gradient(to right, #080112, #23064f); color: white; border-radius: 20px;">
    <tr>
      <td>
        <div>About Breitbart News Network</div>
      </td>
    </tr>
    <tr>
      <td>
        <div>American far-right syndicated news, opinion, and commentary website founded in mid-2007 </div>
      </td>
    </tr>
   </table>
   <br>
   <table style="background-image: linear-gradient(to right, #080112, #23064f); color: white; border-radius: 20px;">
    <tr>
      <td>
        <div>About The Guardian</div>
      </td>
      
    </tr>
    <tr>
      <td>
        <div>British daily newspaper founded in Manchester in 1821 as The Manchester Guardian and changed its name in 1959</div>
      </td>
    </tr>
   </table>
   
  </div>
</template>

<script setup>
// Simple component - no additional logic needed
</script>

<style scoped>
.news-source-info {
  
  text-align: center;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  
  border-radius: 20px;
  padding: 10px;
  margin: 10px;
  background-color: #f0f0f0;
  width: 100%;
  height: 100%;
}

td, th{
    border-radius: 20px;
    padding: 10px;
    margin: 10px;    
    width: 100%;
    height: 100%;
}
</style> 