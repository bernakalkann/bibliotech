<template>
  <div class="container py-2 animated-fade-in" style="max-width: 800px;">
    <!-- Back Navigation Header -->
    <div class="d-flex align-items-center mb-4">
      <router-link to="/" class="premium-btn-secondary px-3 py-2">
        <i class="bi bi-arrow-left"></i> Geri Dön
      </router-link>
      <span class="ms-3 text-muted">/ Kitabı Düzenle</span>
    </div>

    <!-- Main Edit Form Card -->
    <div class="premium-card p-4 shadow-lg">
      <div class="d-flex align-items-center gap-3 mb-4">
        <div class="stat-icon-box" style="background: rgba(245, 158, 11, 0.1); color: var(--status-warning);">
          <i class="bi bi-pencil-square"></i>
        </div>
        <div>
          <h2 class="fw-bold mb-1" style="font-family: var(--font-heading);">Kitabı Düzenle</h2>
          <p class="text-secondary mb-0">Kitap envanter bilgilerini güncelleyin.</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-warning" role="status">
          <span class="visually-hidden">Yükleniyor...</span>
        </div>
        <p class="text-secondary mt-2">Kitap bilgileri alınıyor...</p>
      </div>

      <form v-else @submit.prevent="guncelle">
        <!-- Basic Title and Author -->
        <div class="row">
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Kitap Başlığı</label>
            <div class="position-relative">
              <i class="bi bi-journal-text text-muted style-input-icon"></i>
              <input 
                v-model="kitap.baslik" 
                type="text" 
                class="premium-input ps-5" 
                required 
              />
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Yazar</label>
            <div class="position-relative">
              <i class="bi bi-person text-muted style-input-icon"></i>
              <input 
                v-model="kitap.yazar" 
                type="text" 
                class="premium-input ps-5" 
                required 
              />
            </div>
          </div>
        </div>
        
        <!-- SKU & Price -->
        <div class="row">
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Stok Kodu (SKU)</label>
            <div class="position-relative">
              <i class="bi bi-upc-scan text-muted style-input-icon"></i>
              <input 
                v-model="kitap.sku" 
                type="text" 
                class="premium-input ps-5" 
                required 
              />
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Fiyat (TL)</label>
            <div class="position-relative">
              <i class="bi bi-tags text-muted style-input-icon"></i>
              <input 
                v-model="kitap.fiyat" 
                type="number" 
                step="0.01" 
                min="0"
                class="premium-input ps-5" 
                required 
              />
            </div>
          </div>
        </div>

        <!-- Stock and Supplier -->
        <div class="row">
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Stok Adedi</label>
            <div class="position-relative">
              <i class="bi bi-box-seam text-muted style-input-icon"></i>
              <input 
                v-model="kitap.adet" 
                type="number" 
                min="0"
                class="premium-input ps-5" 
                required 
              />
            </div>
            <!-- Stock level helper slider -->
            <div class="mt-2 px-1 d-flex justify-content-between align-items-center">
              <span class="text-muted" style="font-size: 0.75rem;">Stok Seviyesi</span>
              <span :class="getStockLevelClass(kitap.adet)" style="font-size: 0.75rem; font-weight: 700;">
                {{ getStockLevelText(kitap.adet) }}
              </span>
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Tedarikçi Firma</label>
            <div class="position-relative">
              <i class="bi bi-building text-muted style-input-icon"></i>
              <input 
                v-model="kitap.tedarikci" 
                type="text" 
                class="premium-input ps-5" 
                required 
              />
            </div>
          </div>
        </div>

        <!-- Submit Button Group -->
        <div class="d-flex justify-content-end gap-3 mt-4 pt-4 border-top border-secondary border-opacity-10">
          <router-link to="/" class="premium-btn-secondary px-4 py-2.5">
            İptal
          </router-link>
          <button type="submit" class="premium-btn px-5 py-2.5" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); box-shadow: 0 0 20px rgba(245, 158, 11, 0.35);">
            <i class="bi bi-save-fill"></i> Değişiklikleri Kaydet
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const showToast = inject('showToast', () => {});

const kitap = ref({ baslik: '', yazar: '', sku: '', fiyat: 0, adet: 0, tedarikci: '', fav: false });
const loading = ref(true);

// Sayfa açıldığında kitabın mevcut bilgilerini getir
onMounted(async () => {
  const id = route.params.id;
  loading.value = true;
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/kitaplar/${id}/`);
    kitap.value = res.data;
  } catch (err) {
    showToast("Kitap bilgileri yüklenemedi!", "error");
  } finally {
    loading.value = false;
  }
});

// Güncelleme isteğini gönder
const guncelle = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/kitaplar/${route.params.id}/`, kitap.value, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` }
    });
    showToast('Kitap başarıyla güncellendi.', 'success');
    router.push('/'); // İşlem bitince anasayfaya dön
  } catch (err) {
    showToast('Güncelleme başarısız! Lütfen giriş yaptığınızdan emin olun.', 'error');
  }
};

// Stock levels text helper
const getStockLevelText = (count) => {
  const qty = parseInt(count) || 0;
  if (qty === 0) return 'Tükendi';
  if (qty <= 10) return 'Düşük Stok (Kritik)';
  return 'Yeterli Stok';
};

const getStockLevelClass = (count) => {
  const qty = parseInt(count) || 0;
  if (qty === 0) return 'text-danger';
  if (qty <= 10) return 'text-warning';
  return 'text-success';
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
</style>