<template>
  <div class="container py-2 animated-fade-in">
    <!-- Back Navigation Header -->
    <div class="d-flex align-items-center mb-4">
      <router-link to="/" class="premium-btn-secondary px-3 py-2">
        <i class="bi bi-arrow-left"></i> Geri Dön
      </router-link>
      <span class="ms-3 text-muted">/ Kitap Detayları</span>
    </div>

    <!-- Error/Loading states -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Yükleniyor...</span>
      </div>
      <p class="text-secondary mt-3">Kitap bilgileri sunucudan alınıyor...</p>
    </div>

    <div v-else-if="hata" class="alert alert-danger rounded-4 p-4 shadow-sm">
      <i class="bi bi-exclamation-octagon-fill fs-4 me-2"></i>
      <span>{{ hata }}</span>
    </div>

    <div v-else-if="kitap" class="row g-5">
      <!-- Left Column: Big Showcase Cover -->
      <div class="col-12 col-lg-4">
        <div class="premium-card text-center p-4 d-flex flex-column align-items-center">
          
          <!-- Large Book Cover mockup -->
          <div class="showcase-cover" :class="getGradientClass(kitap.baslik)">
            <span class="showcase-sku">{{ kitap.sku || 'SKU-NONE' }}</span>
            <div class="text-start">
              <h2 class="showcase-title">{{ kitap.baslik }}</h2>
              <p class="showcase-author">{{ kitap.yazar }}</p>
            </div>
            <i class="bi bi-book-half showcase-spine-icon"></i>
          </div>

          <!-- Quick Fav Action -->
          <button 
            @click="toggleFavorite" 
            class="premium-btn-secondary w-100 mt-4 d-flex align-items-center justify-content-center gap-2"
          >
            <i :class="kitap.fav ? 'bi bi-star-fill text-warning' : 'bi bi-star'"></i>
            <span>{{ kitap.fav ? 'Favorilerden Çıkar' : 'Favorilere Ekle' }}</span>
          </button>
        </div>
      </div>

      <!-- Right Column: Detail Metadata -->
      <div class="col-12 col-lg-8">
        <div class="premium-card p-4 h-100 d-flex flex-column justify-content-between">
          <div>
            <div class="d-flex justify-content-between align-items-start mb-4">
              <div>
                <span class="text-secondary uppercase fw-semibold" style="font-size: 0.85rem;">Kitap Başlığı</span>
                <h1 class="h2 fw-bold mt-1 text-primary">{{ kitap.baslik }}</h1>
                <p class="text-muted fs-5 mb-0">Yazar: <strong class="text-light">{{ kitap.yazar }}</strong></p>
              </div>
              <span :class="getStockBadgeClass(kitap.adet)">
                {{ getStockText(kitap.adet) }}
              </span>
            </div>

            <hr class="border-secondary border-opacity-25 mb-4">

            <!-- Detail grid data -->
            <div class="row g-4 mb-4">
              <div class="col-sm-6">
                <div class="detail-item-box">
                  <div class="text-secondary mb-1" style="font-size: 0.85rem;"><i class="bi bi-upc-scan me-1"></i> Stok Kodu (SKU)</div>
                  <code class="fs-5 font-monospace text-info">{{ kitap.sku || 'Belirtilmemiş' }}</code>
                </div>
              </div>

              <div class="col-sm-6">
                <div class="detail-item-box">
                  <div class="text-secondary mb-1" style="font-size: 0.85rem;"><i class="bi bi-tags me-1"></i> Fiyat</div>
                  <strong class="fs-4 text-success">{{ formatCurrency(kitap.fiyat) }}</strong>
                </div>
              </div>

              <div class="col-sm-6">
                <div class="detail-item-box">
                  <div class="text-secondary mb-1" style="font-size: 0.85rem;"><i class="bi bi-building me-1"></i> Tedarikçi Firma</div>
                  <span class="fs-5 text-light fw-semibold">{{ kitap.tedarikci || 'Belirtilmemiş' }}</span>
                </div>
              </div>

              <div class="col-sm-6">
                <div class="detail-item-box">
                  <div class="text-secondary mb-1" style="font-size: 0.85rem;"><i class="bi bi-box-seam me-1"></i> Stok Seviyesi</div>
                  <div class="d-flex align-items-center gap-3 mt-1">
                    <strong class="fs-5 text-light">{{ kitap.adet || 0 }} Adet</strong>
                    <!-- Inventory fill bar indicator -->
                    <div class="progress flex-grow-1" style="height: 8px; background-color: rgba(255,255,255,0.05); border-radius: 99px;">
                      <div 
                        class="progress-bar" 
                        :class="getStockBarColorClass(kitap.adet)" 
                        :style="{ width: Math.min(((kitap.adet || 0) / 100) * 100, 100) + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom controls -->
          <div class="d-flex justify-content-end gap-3 mt-4 pt-4 border-top border-secondary border-opacity-10">
            <router-link 
              :to="{ name: 'KitapDuzenle', params: { id: kitap.id } }" 
              class="premium-btn px-4 py-2.5"
            >
              <i class="bi bi-pencil-square"></i> Düzenle
            </router-link>
            <button 
              @click="sil" 
              class="btn btn-outline-danger px-4 py-2.5 rounded-3 fw-semibold d-flex align-items-center gap-2"
            >
              <i class="bi bi-trash3"></i> Sil
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const showToast = inject('showToast', () => {});

const kitap = ref(null);
const loading = ref(true);
const hata = ref(null);

// Fetch book details on page mount
const fetchKitap = async () => {
  const id = route.params.id;
  loading.value = true;
  hata.value = null;
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/kitaplar/${id}/`);
    kitap.value = res.data;
  } catch (err) {
    hata.value = "Kitap bilgileri sunucudan yüklenemedi!";
    showToast("Kitap bilgileri yüklenemedi!", "error");
  } finally {
    loading.value = false;
  }
};

// Toggle favorite state
const toggleFavorite = async () => {
  if (!kitap.value) return;
  kitap.value.fav = !kitap.value.fav;
  try {
    await axios.put(`http://127.0.0.1:8000/api/kitaplar/${kitap.value.id}/`, kitap.value, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` }
    });
    showToast(
      kitap.value.fav ? `"${kitap.value.baslik}" favorilere eklendi.` : `"${kitap.value.baslik}" favorilerden çıkarıldı.`,
      'success'
    );
  } catch (err) {
    // Revert state on error
    kitap.value.fav = !kitap.value.fav;
    showToast("İşlem gerçekleştirilemedi, giriş yaptığınızdan emin olun.", "warning");
  }
};

// Delete action
const sil = async () => {
  if (!kitap.value) return;
  if (confirm("Bu kitabı silmek istediğinize emin misiniz?")) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/kitaplar/${kitap.value.id}/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` }
      });
      showToast('Kitap başarıyla silindi.', 'success');
      router.push('/');
    } catch (err) {
      showToast('Silme işlemi başarısız, giriş yapıp yapmadığınızı kontrol edin!', 'error');
    }
  }
};

onMounted(fetchKitap);

// Formatting helpers
const formatCurrency = (val) => {
  const fiyat = parseFloat(val) || 0;
  return fiyat.toLocaleString('tr-TR', { style: 'currency', currency: 'TRY' });
};

const getGradientClass = (title) => {
  if (!title) return 'book-cover-grad-1';
  const code = title.charCodeAt(0) || 0;
  const num = (code % 6) + 1;
  return `book-cover-grad-${num}`;
};

const getStockBadgeClass = (count) => {
  const stock = parseInt(count) || 0;
  if (stock > 10) return 'badge-status badge-instock';
  if (stock > 0) return 'badge-status badge-lowstock';
  return 'badge-status badge-outstock';
};

const getStockText = (count) => {
  const stock = parseInt(count) || 0;
  if (stock > 10) return 'Stokta Var';
  if (stock > 0) return `Son ${stock} Ürün`;
  return 'Tükendi';
};

const getStockBarColorClass = (count) => {
  const stock = parseInt(count) || 0;
  if (stock > 10) return 'bg-success';
  if (stock > 0) return 'bg-warning';
  return 'bg-danger';
};
</script>

<style scoped>
/* Large 3D showcase cover rules */
.showcase-cover {
  width: 220px;
  aspect-ratio: 2/3;
  border-radius: 16px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.showcase-cover::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 18px;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.3) 0%, rgba(255, 255, 255, 0.1) 40%, rgba(0, 0, 0, 0.05) 60%, transparent 100%);
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
}

.showcase-title {
  font-family: var(--font-heading);
  font-weight: 800;
  color: #fff;
  font-size: 1.5rem;
  line-height: 1.25;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
  z-index: 2;
  margin-top: 1rem;
}

.showcase-author {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
  z-index: 2;
  margin-bottom: 0;
}

.showcase-sku {
  font-size: 0.75rem;
  background: rgba(0,0,0,0.4);
  color: rgba(255,255,255,0.8);
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.5px;
  align-self: flex-start;
}

.showcase-spine-icon {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  font-size: 2.5rem;
  color: rgba(255,255,255,0.15);
  z-index: 1;
}

/* Item boxes */
.detail-item-box {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-color);
  padding: 1.25rem;
  border-radius: 16px;
  height: 100%;
}
</style>