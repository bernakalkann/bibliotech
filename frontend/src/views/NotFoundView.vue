<template>
  <div class="container d-flex align-items-center justify-content-center animated-fade-in" style="min-height: 80vh;">
    <!-- Centered Glassmorphic 404 Box -->
    <div class="premium-card p-5 w-100 text-center shadow-lg position-relative" style="max-width: 500px;">
      
      <!-- Big Glowing 404 Text -->
      <h1 class="glow-text mb-2">404</h1>
      
      <div class="d-inline-flex align-items-center justify-content-center rounded-circle mb-3 text-danger bg-danger bg-opacity-10 p-3" style="width: 60px; height: 60px;">
        <i class="bi bi-exclamation-triangle-fill fs-3"></i>
      </div>

      <h3 class="fw-bold mb-2">Sayfa Bulunamadı</h3>
      <p class="text-secondary mb-4 mx-auto" style="max-width: 320px; font-size: 0.95rem;">
        Aradığınız sayfa silinmiş, taşınmış veya geçici olarak kullanım dışı olabilir.
      </p>

      <router-link to="/" class="premium-btn px-4 py-2.5">
        <i class="bi bi-house-door-fill"></i> Anasayfaya Dön
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.glow-text {
  font-size: 6.5rem;
  font-weight: 900;
  line-height: 1;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 10px rgba(168, 85, 247, 0.4));
  margin: 0;
  letter-spacing: -2px;
}
</style>