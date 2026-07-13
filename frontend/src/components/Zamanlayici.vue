<template>
  <div class="box">
    <p>Zaman ilerliyor... {{ zaman }} ms</p>
    
    <button @click="durdur">Okumayı Bitir</button>
  </div>
</template>

<script>
export default {
  data() { 
    return { zaman: 0, timer: null } 
  },
  mounted() {
    // Bileşen ekrana geldiği an sayacı başlat
    this.timer = setInterval(() => { this.zaman += 10 }, 10);
  },
  methods: {
    durdur() {
      // Zamanlayıcıyı durdur
      clearInterval(this.timer);
      // Ana bileşene "bittim ve sürem şu" diye haber ver
      this.$emit('bitir', this.zaman); 
    }
  }
}
</script>

<style scoped>
.box {
  padding: 20px;
  background: #f0f0f0;
  margin-top: 10px;
  border-radius: 8px;
  text-align: center;
}
</style>