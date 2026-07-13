<template>
  <div class="container py-2 animated-fade-in" style="max-width: 800px;">
    <!-- Back Navigation Header -->
    <div class="d-flex align-items-center mb-4">
      <router-link to="/" class="premium-btn-secondary px-3 py-2">
        <i class="bi bi-arrow-left"></i> Geri Dön
      </router-link>
      <span class="ms-3 text-muted">/ Yeni Kitap Ekle</span>
    </div>

    <!-- Main Creation Form Card -->
    <div class="premium-card p-4 shadow-lg">
      <div class="d-flex align-items-center gap-3 mb-4">
        <div class="stat-icon-box" style="background: rgba(168, 85, 247, 0.1); color: var(--accent-color);">
          <i class="bi bi-plus-square-fill"></i>
        </div>
        <div>
          <h2 class="fw-bold mb-1" style="font-family: var(--font-heading);">Yeni Kitap Ekle</h2>
          <p class="text-secondary mb-0">Envantere yeni bir kitap kaydetmek için aşağıdaki alanları doldurun.</p>
        </div>
      </div>

      <form @submit.prevent="ekle" class="needs-validation">
        <!-- Basic Title and Author -->
        <div class="row">
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Kitap Başlığı</label>
            <div class="position-relative">
              <i class="bi bi-journal-text text-muted style-input-icon"></i>
              <input 
                v-model="yeniKitap.baslik" 
                type="text" 
                class="premium-input ps-5" 
                placeholder="Örn: Nutuk" 
                required 
              />
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Yazar</label>
            <div class="position-relative">
              <i class="bi bi-person text-muted style-input-icon"></i>
              <input 
                v-model="yeniKitap.yazar" 
                type="text" 
                class="premium-input ps-5" 
                placeholder="Örn: Mustafa Kemal Atatürk" 
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
                v-model="yeniKitap.sku" 
                type="text" 
                class="premium-input ps-5" 
                placeholder="Örn: SKU-NUTUK-1927" 
                required 
              />
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Fiyat (TL)</label>
            <div class="position-relative">
              <i class="bi bi-tags text-muted style-input-icon"></i>
              <input 
                v-model="yeniKitap.fiyat" 
                type="number" 
                step="0.01" 
                min="0"
                class="premium-input ps-5" 
                placeholder="0.00" 
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
                v-model="yeniKitap.adet" 
                type="number" 
                min="0"
                class="premium-input ps-5" 
                placeholder="0" 
                required 
              />
            </div>
            <!-- Stock level helper slider -->
            <div class="mt-2 px-1 d-flex justify-content-between align-items-center">
              <span class="text-muted" style="font-size: 0.75rem;">Stok Seviyesi</span>
              <span :class="getStockLevelClass(yeniKitap.adet)" style="font-size: 0.75rem; font-weight: 700;">
                {{ getStockLevelText(yeniKitap.adet) }}
              </span>
            </div>
          </div>
          <div class="col-md-6 mb-4">
            <label class="form-label fw-semibold text-secondary mb-2">Tedarikçi Firma</label>
            <div class="position-relative">
              <i class="bi bi-building text-muted style-input-icon"></i>
              <input 
                v-model="yeniKitap.tedarikci" 
                type="text" 
                class="premium-input ps-5" 
                placeholder="Örn: Yapı Kredi Yayınları" 
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
          <button type="submit" class="premium-btn px-5 py-2.5">
            <i class="bi bi-check-lg"></i> Kitabı Kaydet
          </button>
        </div>
      </form>

      <p v-if="hata" class="alert alert-danger mt-3 rounded-3">{{ hata }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useKitaplar } from '../composables/useKitaplar';
import { useRouter } from 'vue-router';

const { kitapEkle, hata } = useKitaplar();
const router = useRouter();

const showToast = inject('showToast', () => {});

// yeniKitap objesini modeldeki tüm alanlarla güncelledik
const yeniKitap = ref({ 
  baslik: '', 
  yazar: '', 
  sku: '', 
  fiyat: 0, 
  adet: 0, 
  tedarikci: '',
  fav: false 
});

const ekle = async () => {
  await kitapEkle(yeniKitap.value);
  if (!hata.value) {
    showToast('Kitap başarıyla envantere eklendi.', 'success');
    router.push('/'); // Başarılıysa listeye dön
  } else {
    showToast('Kitap eklenirken bir hata oluştu: ' + hata.value, 'error');
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