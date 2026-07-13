<template>
  <div class="container d-flex align-items-center justify-content-center animated-fade-in" style="min-height: 80vh;">
    <!-- Centered Glassmorphic Login Box -->
    <div class="premium-card p-5 w-100 shadow-lg position-relative" style="max-width: 450px;">
      
      <!-- Glowing decorative light effect inside the card -->
      <div class="glow-decoration"></div>

      <!-- Icon & Header -->
      <div class="text-center mb-4 position-relative" style="z-index: 2;">
        <div class="d-inline-flex align-items-center justify-content-center rounded-circle mb-3 text-white" style="width: 70px; height: 70px; background: var(--accent-gradient); box-shadow: var(--accent-glow);">
          <i class="bi bi-shield-lock-fill fs-2"></i>
        </div>
        <h2 class="fw-bold mb-1" style="font-family: var(--font-heading);">Sistem Girişi</h2>
        <p class="text-secondary" style="font-size: 0.9rem;">Kitap yönetimi işlemlerini gerçekleştirmek için oturum açın.</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="girisYap" class="position-relative" style="z-index: 2;">
        <!-- Username input -->
        <div class="premium-input-group mb-3">
          <label class="form-label text-secondary fw-semibold mb-2" style="font-size: 0.85rem;">Kullanıcı Adı</label>
          <div class="position-relative">
            <i class="bi bi-person text-muted style-input-icon"></i>
            <input 
              v-model="credentials.username" 
              type="text"
              class="premium-input ps-5" 
              placeholder="Yönetici kullanıcı adınız" 
              required 
            />
          </div>
        </div>

        <!-- Password input -->
        <div class="premium-input-group mb-4">
          <label class="form-label text-secondary fw-semibold mb-2" style="font-size: 0.85rem;">Şifre</label>
          <div class="position-relative">
            <i class="bi bi-key text-muted style-input-icon"></i>
            <input 
              v-model="credentials.password" 
              type="password" 
              class="premium-input ps-5" 
              placeholder="••••••••" 
              required 
            />
          </div>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="premium-btn w-100 py-3 shadow-lg" :disabled="submitting">
          <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          <i v-else class="bi bi-box-arrow-in-right me-1"></i>
          Giriş Yap
        </button>
      </form>

      <!-- Cancel/Back button -->
      <div class="text-center mt-4 position-relative" style="z-index: 2;">
        <router-link to="/" class="text-secondary text-decoration-none hover-white" style="font-size: 0.85rem;">
          <i class="bi bi-arrow-left"></i> Ziyaretçi olarak devam et
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const credentials = ref({ username: '', password: '' });
const router = useRouter();
const submitting = ref(false);

const showToast = inject('showToast', () => {});

const girisYap = async () => {
  submitting.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/token/', credentials.value);
    // Token'ı tarayıcıya kaydet
    localStorage.setItem('access', response.data.access);
    showToast("Giriş başarıyla sağlandı. Yönetim yetkileri aktifleştirildi.", "success");
    router.push('/'); // Başarılıysa anasayfaya dön
  } catch (error) {
    showToast("Giriş başarısız! Bilgilerinizi kontrol edin.", "error");
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.style-input-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

/* Background glowing decoration circle */
.glow-decoration {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.25) 0%, transparent 70%);
  z-index: 1;
  pointer-events: none;
  filter: blur(20px);
}

.hover-white:hover {
  color: var(--text-primary) !important;
  transition: var(--transition-smooth);
}
</style>