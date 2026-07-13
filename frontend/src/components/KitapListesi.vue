<template>
  <div v-if="hata" class="alert alert-danger rounded-4 shadow-sm my-3 border-danger border-opacity-25 d-flex align-items-center gap-2">
    <i class="bi bi-exclamation-triangle-fill fs-5"></i>
    <span>{{ hata }}</span>
  </div>

  <!-- Empty State Placeholder -->
  <div v-if="!kitaplar || kitaplar.length === 0" class="premium-card text-center py-5 my-4">
    <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-secondary bg-opacity-10 p-4 mb-4 text-secondary" style="width: 80px; height: 80px;">
      <i class="bi bi-journal-x fs-1"></i>
    </div>
    <h3 class="fw-bold mb-2">Herhangi Bir Kitap Bulunmadı</h3>
    <p class="text-secondary mx-auto mb-4" style="max-width: 400px;">
      Kütüphanede henüz kayıtlı kitap yok veya arama filtrelerinize uygun bir sonuç bulunamadı.
    </p>
    <router-link to="/ekle" class="premium-btn">
      <i class="bi bi-plus-lg"></i> Yeni Kitap Ekle
    </router-link>
  </div>

  <!-- Dual View Container -->
  <div v-else>
    <!-- 1. GRID VIEW MODE -->
    <div v-if="viewMode === 'grid'" class="row g-4 my-2">
      <div v-for="kitap in kitaplar" :key="kitap.id" class="col-12 col-md-6 col-lg-4 col-xl-3">
        <div class="premium-card h-100 d-flex flex-column justify-content-between p-3 position-relative">
          
          <!-- Favorite toggle button (positioned absolutely) -->
          <button 
            @click.stop="$emit('favori-degisti', kitap)" 
            class="fav-badge btn btn-link"
            title="Favori Durumu"
          >
            <i :class="kitap.fav ? 'bi bi-star-fill text-warning' : 'bi bi-star text-white-50'"></i>
          </button>

          <div>
            <!-- Deterministic Gradients for book covers -->
            <div class="book-cover" :class="getGradientClass(kitap.baslik)">
              <div class="d-flex justify-content-between align-items-start w-100">
                <span class="sku-badge font-monospace">{{ kitap.sku || 'SKU-NONE' }}</span>
                <span class="price-badge">{{ formatCurrency(kitap.fiyat) }}</span>
              </div>
              <div>
                <h4 class="book-cover-title text-truncate-2">{{ kitap.baslik }}</h4>
                <div class="book-cover-author mt-1 text-truncate">{{ kitap.yazar }}</div>
              </div>
            </div>

            <!-- Meta details under the cover -->
            <div class="px-1 mt-2">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="text-muted text-truncate" style="font-size: 0.8rem;">
                  <i class="bi bi-building me-1"></i> {{ kitap.tedarikci || 'Tedarikçi Belirtilmemiş' }}
                </span>
                
                <!-- Stock status badge -->
                <span :class="getStockBadgeClass(kitap.adet)">
                  {{ getStockText(kitap.adet) }}
                </span>
              </div>

              <!-- Inventory stock gauge bar -->
              <div class="stock-gauge-wrapper mb-3">
                <div class="d-flex justify-content-between style-gauge-label mb-1">
                  <span>Stok Durumu</span>
                  <span>{{ kitap.adet || 0 }} adet</span>
                </div>
                <div class="progress" style="height: 6px; background-color: rgba(255,255,255,0.05); border-radius: 99px;">
                  <div 
                    class="progress-bar" 
                    role="progressbar" 
                    :class="getStockBarColorClass(kitap.adet)"
                    :style="{ width: Math.min(((kitap.adet || 0) / 100) * 100, 100) + '%' }"
                    aria-valuenow="0" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Slots description if it passes -->
          <div class="card-slot-content px-1 mb-3">
            <slot />
          </div>

          <!-- Grid Footer controls -->
          <div class="d-flex gap-2 mt-auto px-1 pt-2 border-top border-secondary border-opacity-10">
            <router-link 
              :to="{ name: 'KitapDetay', params: { id: kitap.id } }" 
              class="btn btn-sm btn-outline-info flex-grow-1 rounded-3 py-2 d-flex align-items-center justify-content-center gap-1"
            >
              <i class="bi bi-eye"></i> Detay
            </router-link>
            <router-link 
              :to="{ name: 'KitapDuzenle', params: { id: kitap.id } }" 
              class="btn btn-sm btn-outline-warning rounded-3 px-3 py-2"
              title="Kitap Düzenle"
            >
              <i class="bi bi-pencil-square"></i>
            </router-link>
            <button 
              @click="$emit('sil', kitap.id)" 
              class="btn btn-sm btn-outline-danger rounded-3 px-3 py-2"
              title="Kitap Sil"
            >
              <i class="bi bi-trash3"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. TABLE VIEW MODE -->
    <div v-else class="premium-card p-0 overflow-hidden my-4">
      <div class="table-responsive">
        <table class="table table-hover table-premium align-middle mb-0">
          <thead>
            <tr>
              <th scope="col" style="width: 40px;" class="ps-4"></th>
              <th scope="col">Başlık</th>
              <th scope="col">Yazar</th>
              <th scope="col">SKU (Stok Kodu)</th>
              <th scope="col">Fiyat</th>
              <th scope="col">Stok Adedi</th>
              <th scope="col">Tedarikçi</th>
              <th scope="col">Durum</th>
              <th scope="col" class="text-end pe-4" style="width: 250px;">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="kitap in kitaplar" :key="kitap.id">
              <td class="ps-4 text-center">
                <!-- Inline star toggler -->
                <button 
                  @click.stop="$emit('favori-degisti', kitap)" 
                  class="btn btn-link p-0 m-0 border-0 text-decoration-none"
                >
                  <i :class="kitap.fav ? 'bi bi-star-fill text-warning' : 'bi bi-star text-white-50'"></i>
                </button>
              </td>
              <td>
                <router-link 
                  :to="{ name: 'KitapDetay', params: { id: kitap.id } }"
                  class="fw-bold text-decoration-none"
                  style="color: var(--text-primary);"
                >
                  {{ kitap.baslik }}
                </router-link>
              </td>
              <td class="text-secondary">{{ kitap.yazar }}</td>
              <td><code class="font-monospace text-info bg-opacity-10 px-2 py-1 rounded" style="font-size: 0.8rem; background: rgba(14,165,233,0.1);">{{ kitap.sku || '-' }}</code></td>
              <td class="fw-semibold">{{ formatCurrency(kitap.fiyat) }}</td>
              <td class="font-monospace">{{ kitap.adet }}</td>
              <td class="text-secondary">{{ kitap.tedarikci || '-' }}</td>
              <td>
                <span :class="getStockBadgeClass(kitap.adet)">
                  {{ getStockText(kitap.adet) }}
                </span>
              </td>
              <td class="text-end pe-4">
                <router-link 
                  :to="{ name: 'KitapDetay', params: { id: kitap.id } }" 
                  class="btn btn-sm btn-outline-info me-2 rounded-3"
                >
                  <i class="bi bi-eye"></i> İncele
                </router-link>
                <router-link 
                  :to="{ name: 'KitapDuzenle', params: { id: kitap.id } }" 
                  class="btn btn-sm btn-warning me-2 rounded-3"
                >
                  <i class="bi bi-pencil-square"></i> Düzenle
                </router-link>
                <button 
                  @click="$emit('sil', kitap.id)" 
                  class="btn btn-sm btn-danger rounded-3"
                >
                  <i class="bi bi-trash3"></i> Sil
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props: HomeView'dan gelen verileri burada karşılıyoruz (Dokunulmadı)
// Emits: Silme isteğini yukarı iletiyoruz (Dokunulmadı)
defineProps({
  kitaplar: {
    type: Array,
    required: true
  },
  hata: {
    type: String,
    default: null
  },
  viewMode: {
    type: String,
    default: 'grid'
  }
});

defineEmits(['sil', 'favori-degisti']);

// Formatting currency in Turkish Liras
const formatCurrency = (value) => {
  const fiyat = parseFloat(value) || 0;
  return fiyat.toLocaleString('tr-TR', { style: 'currency', currency: 'TRY' });
};

// Deterministic Gradient Class assignment for Book Covers
const getGradientClass = (title) => {
  if (!title) return 'book-cover-grad-1';
  const code = title.charCodeAt(0) || 0;
  const num = (code % 6) + 1; // 1 to 6 gradient options
  return `book-cover-grad-${num}`;
};

// Stock logic styles helper
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
/* Star icon container absolute styles */
.fav-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
  font-size: 1.35rem;
  padding: 0;
  margin: 0;
  text-decoration: none;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5));
  transition: all 0.2s ease;
}

.fav-badge:hover {
  transform: scale(1.2);
}

/* Card custom list labels */
.style-gauge-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 600;
}

/* Text truncate helpers */
.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sku-badge {
  font-size: 0.7rem;
  background: rgba(0,0,0,0.3);
  color: rgba(255,255,255,0.7);
  padding: 3px 8px;
  border-radius: 6px;
  letter-spacing: 0.5px;
}

.price-badge {
  font-size: 0.8rem;
  background: var(--accent-gradient);
  color: #fff;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(168,85,247,0.3);
}
</style>
