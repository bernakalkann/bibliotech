<template>
  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <div>
        <!-- Logo Branding -->
        <div class="brand">
          <i class="bi bi-book-half brand-icon"></i>
          <span class="brand-title">Bibliotech</span>
        </div>

        <!-- Navigation Menu -->
        <nav>
          <ul class="nav-menu">
            <li>
              <router-link to="/" class="nav-item-link">
                <i class="bi bi-grid-1x2-fill"></i>
                <span class="nav-item-text">Kontrol Paneli</span>
              </router-link>
            </li>
            <li>
              <router-link to="/ekle" class="nav-item-link">
                <i class="bi bi-plus-circle-fill"></i>
                <span class="nav-item-text">Yeni Kitap Ekle</span>
              </router-link>
            </li>
            <li>
              <router-link to="/hakkimizda" class="nav-item-link">
                <i class="bi bi-info-circle-fill"></i>
                <span class="nav-item-text">Hakkımızda</span>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>

      <!-- User & Profile Controls / Theme Toggle -->
      <div class="sidebar-footer">
        <!-- Theme Toggle Button -->
        <button @click="toggleTheme" class="btn btn-link nav-item-link w-100 border-0 mb-3 justify-content-start text-start" style="cursor: pointer; background: transparent;">
          <i :class="isDark ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill text-primary'"></i>
          <span class="nav-item-text">{{ isDark ? 'Açık Mod' : 'Karanlık Mod' }}</span>
        </button>

        <!-- Auth Controls -->
        <div v-if="isLoggedIn" class="user-profile flex-column align-items-stretch gap-2">
          <div class="d-flex align-items-center gap-2">
            <div class="avatar">
              {{ username.charAt(0).toUpperCase() }}
            </div>
            <div class="user-name overflow-hidden">
              <div class="fw-bold text-truncate" style="font-size: 0.9rem;">{{ username }}</div>
              <div class="text-muted" style="font-size: 0.75rem;">Yönetici</div>
            </div>
          </div>
          <button @click="logout" class="btn btn-outline-danger btn-sm w-100 rounded-3 mt-2 py-1.5 d-flex align-items-center justify-content-center gap-1">
            <i class="bi bi-box-arrow-right"></i>
            <span class="nav-item-text">Çıkış Yap</span>
          </button>
        </div>
        <div v-else>
          <router-link to="/giris" class="nav-item-link justify-content-center text-center bg-primary text-white border-0 py-2 shadow-sm">
            <i class="bi bi-box-arrow-in-right"></i>
            <span class="nav-item-text">Giriş Yap</span>
          </router-link>
        </div>
      </div>
    </aside>

    <!-- Main Content Panel -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Custom Toast Notifications Overlay -->
    <transition name="toast-anim">
      <div v-if="toastState.show" class="toast-container-custom" :class="toastState.type">
        <i :class="toastIcon"></i>
        <span>{{ toastState.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, provide, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Theme State (Dark by default)
const isDark = ref(true);

const toggleTheme = () => {
  isDark.value = !isDark.value;
  const theme = isDark.value ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
};

// Authentication State
const isLoggedIn = ref(false);
const username = ref('Admin User');

const checkLoginStatus = () => {
  const token = localStorage.getItem('access');
  isLoggedIn.value = !!token;
  if (token) {
    // Basic username parsing or mock
    username.value = 'Kütüphane Görevlisi';
  }
};

const logout = () => {
  localStorage.removeItem('access');
  isLoggedIn.value = false;
  showToast('Başarıyla çıkış yapıldı.', 'info');
  router.push('/giris');
};

// Listen to route changes to update authentication state
watch(() => route.path, () => {
  checkLoginStatus();
});

// Toast System
const toastState = reactive({
  show: false,
  message: '',
  type: 'success' // success, error, info, warning
});

const showToast = (message, type = 'success') => {
  toastState.message = message;
  toastState.type = type;
  toastState.show = true;
  
  // Auto dismiss
  setTimeout(() => {
    toastState.show = false;
  }, 4000);
};

// Provide toast method globally to all children components
provide('showToast', showToast);

const toastIcon = computed(() => {
  switch (toastState.type) {
    case 'success': return 'bi bi-check-circle-fill fs-5';
    case 'error': return 'bi bi-x-circle-fill fs-5';
    case 'warning': return 'bi bi-exclamation-triangle-fill fs-5';
    default: return 'bi bi-info-circle-fill fs-5';
  }
});

onMounted(() => {
  // Read and apply theme
  const savedTheme = localStorage.getItem('theme') || 'dark';
  isDark.value = savedTheme === 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  checkLoginStatus();
});
</script>

<style scoped>
/* Sidebar and layouts */
.sidebar-footer {
  margin-top: auto;
}

/* Toast styling */
.toast-container-custom {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 16px 24px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 9999;
  font-weight: 600;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255,255,255,0.1);
  color: white;
}

.toast-container-custom.success {
  background: rgba(16, 185, 129, 0.9);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.toast-container-custom.error {
  background: rgba(239, 68, 68, 0.9);
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.3);
}

.toast-container-custom.warning {
  background: rgba(245, 158, 11, 0.9);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3);
}

.toast-container-custom.info {
  background: rgba(14, 165, 233, 0.9);
  box-shadow: 0 8px 24px rgba(14, 165, 233, 0.3);
}

/* Toast animation */
.toast-anim-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}
.toast-anim-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.toast-anim-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.toast-anim-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}
</style>