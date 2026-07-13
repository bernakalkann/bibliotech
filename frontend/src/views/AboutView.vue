<template>
  <div class="container py-2 animated-fade-in" style="max-width: 900px;">
    <!-- Header Page -->
    <div class="mb-5 text-center text-md-start">
      <h1 class="fw-extrabold mb-1" style="font-size: 2.2rem; font-family: var(--font-heading);">Bibliotech Hakkında</h1>
      <p class="text-secondary" style="font-size: 1rem;">Sistem mimarisi, teknoloji yığını ve projenin genel yapısı.</p>
    </div>

    <!-- About Content Grid -->
    <div class="row g-4">
      <div class="col-12 col-md-8">
        <div class="premium-card p-4 h-100">
          <h3 class="fw-bold mb-3 text-primary"><i class="bi bi-info-circle-fill me-2"></i> Sistem Amacı</h3>
          <p class="text-secondary mb-4" style="line-height: 1.6;">
            Bibliotech, modern kütüphanelerin ve dijital kitap arşivlerinin yönetimi için tasarlanmış yüksek performanslı, estetik bir yönetim panelidir. Kitapların envanter kayıtlarını, fiyatlandırmalarını, tedarikçilerini ve stok durumlarını gerçek zamanlı takip edebilmek üzere optimize edilmiştir.
          </p>

          <h3 class="fw-bold mb-3 text-primary"><i class="bi bi-stack me-2"></i> Teknoloji Yığını</h3>
          <div class="row g-3">
            <div class="col-6">
              <div class="p-3 rounded-3 bg-dark border border-secondary border-opacity-10">
                <div class="fw-bold text-light mb-1"><i class="bi bi-lightning-charge-fill text-warning me-1"></i> Frontend</div>
                <div class="text-secondary style-tech-sub">Vue 3 (Composition API)</div>
                <div class="text-secondary style-tech-sub">Vite & Bootstrap 5</div>
              </div>
            </div>
            <div class="col-6">
              <div class="p-3 rounded-3 bg-dark border border-secondary border-opacity-10">
                <div class="fw-bold text-light mb-1"><i class="bi bi-server text-info me-1"></i> Backend</div>
                <div class="text-secondary style-tech-sub">Python (Django)</div>
                <div class="text-secondary style-tech-sub">Django REST Framework</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4">
        <div class="premium-card p-4 h-100 d-flex flex-column justify-content-between">
          <div>
            <h3 class="fw-bold mb-3 text-warning"><i class="bi bi-cpu me-2"></i> Geliştirici</h3>
            <p class="text-secondary" style="font-size: 0.95rem;">
              Bu proje Vue ve Django entegrasyonu eğitim serisi kapsamında modern web arayüz standartlarına uygun olarak tasarlanmıştır.
            </p>
          </div>

          <div class="pt-4 border-top border-secondary border-opacity-10">
            <button @click="anasayfayaGit" class="premium-btn w-100 py-2.5">
              <i class="bi bi-house-door-fill"></i> Kontrol Paneline Dön
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const anasayfayaGit = () => {
  console.log("Hakkımızda sayfasından Kontrol Paneline yönlendiriliyor...");
  router.push('/');
};
</script>

<script>
// We keep backward compatibility with the user's component logic if needed
export default {
  methods: {
    // Declared methods for legacy code safety
    anasayfayaGitLegacy() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.style-tech-sub {
  font-size: 0.8rem;
  font-family: monospace;
}
</style>