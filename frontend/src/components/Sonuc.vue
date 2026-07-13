<template>
  <div class="sonuc-box">
    <p>Oyun Bitti! Süren: {{ skor }} ms</p>
    <p v-if="skor < 300">Harika refleksler! ⚡</p>
    <p v-else>Biraz daha hızlı olabilirsin. 🐢</p>
  </div>
</template>

<script>
export default {
  props: ['skor'] // Ana bileşenden sonucu alıyoruz
}
</script>

<style scoped>
.sonuc-box { color: green; font-weight: bold; margin-top: 10px; }
</style>