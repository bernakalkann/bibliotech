<script setup>
import { ref, computed, watch, watchEffect, reactive, inject } from 'vue';
import { useKitaplar } from '../composables/useKitaplar'; 
import KitapListesi from '../components/KitapListesi.vue';
import Zamanlayici from '../components/Zamanlayici.vue';
import Sonuc from '../components/Sonuc.vue';

// 1. ADIM: Kitaplar için gerekli olanları import ettik (Silme dahil - Dokunulmadı)
const { kitaplar, hata, kitapSil } = useKitaplar();

// Toast notification function injected from App.vue
const showToast = inject('showToast', () => {});

// Layout view mode (grid or list/table)
const viewMode = ref('grid');

// Search and Filter states
const searchQuery = ref('');
const activeFilter = ref('all');

// Computed stats for Dashboard Cards
const kitapSayisi = computed(() => kitaplar.value.length);

const favoriSayisi = computed(() => {
  return kitaplar.value.filter(k => k.fav).length;
});

const toplamStok = computed(() => {
  return kitaplar.value.reduce((acc, k) => acc + (parseInt(k.adet) || 0), 0);
});

const toplamDeger = computed(() => {
  return kitaplar.value.reduce((acc, k) => {
    const fiyat = parseFloat(k.fiyat) || 0;
    const adet = parseInt(k.adet) || 0;
    return acc + (fiyat * adet);
  }, 0);
});

// Computed filtered books list based on search query and active filter
const filtrelenmisKitaplar = computed(() => {
  return kitaplar.value.filter(k => {
    const title = (k.baslik || '').toLowerCase();
    const author = (k.yazar || '').toLowerCase();
    const sku = (k.sku || '').toLowerCase();
    const supplier = (k.tedarikci || '').toLowerCase();
    const query = searchQuery.value.toLowerCase();

    const matchesSearch = title.includes(query) || 
                          author.includes(query) || 
                          sku.includes(query) || 
                          supplier.includes(query);

    if (activeFilter.value === 'fav') {
      return matchesSearch && k.fav;
    } else if (activeFilter.value === 'instock') {
      return matchesSearch && (parseInt(k.adet) > 0);
    } else if (activeFilter.value === 'outstock') {
      return matchesSearch && (!k.adet || parseInt(k.adet) <= 0);
    }

    return matchesSearch;
  });
});

// Silme fonksiyonunu burada tanımlıyoruz (Geliştirildi, orijinal logic korundu)
const sil = async (id) => {
  if (confirm("Bu kitabı silmek istediğinize emin misiniz?")) {
    await kitapSil(id);
    if (!hata.value) {
      showToast('Kitap başarıyla silindi.', 'success');
    } else {
      showToast(hata.value, 'error');
    }
  }
};

// --- EĞİTİM KODLARINIZ (Dokunulmadı) ---
const baslik = ref("Vue Dersleri");
const mesaj = ref("Henüz bir şey yapmadın.");
const sayac = ref(0);
const isimInputu = ref(null);

const oyunDurumu = reactive({
  basliyor: false,
  skor: null,
  bitti: false
});

const sayacMesaji = computed(() => {
  return sayac.value > 5 ? 'Harika, 5\'i geçtin!' : 'Sayı henüz düşük.';
});

watch(sayac, (yeniDeger) => {
  console.log("Sayı güncellendi, yeni değer:", yeniDeger);
});

const degistir = () => {
  mesaj.value = "Butona bastın!";
  sayac.value++;
};

const odaklan = () => {
  isimInputu.value.focus();
};

const favoriDegistir = (kitap) => {
  kitap.fav = !kitap.fav;
  showToast(
    kitap.fav ? `"${kitap.baslik}" favorilere eklendi.` : `"${kitap.baslik}" favorilerden çıkarıldı.`,
    'success'
  );
};

const oyunuBaslat = () => {
  oyunDurumu.basliyor = true;
  oyunDurumu.bitti = false;
};

const sonucuGoster = (zaman) => {
  oyunDurumu.skor = zaman;
  oyunDurumu.basliyor = false;
  oyunDurumu.bitti = true;
};

watch(() => oyunDurumu.bitti, (yeniDeger) => {
  if (yeniDeger) {
    alert("Oyun sona erdi! Skorunuz: " + oyunDurumu.skor);
  }
});

watchEffect(() => {
  console.log("Oyun Durumu güncellendi, şu anki skor: " + oyunDurumu.skor);
});
</script>

<template>
  <div class="container-fluid py-2 animated-fade-in">
    <!-- Header section -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-5 gap-3">
      <div>
        <h1 class="fw-extrabold mb-1" style="font-size: 2.2rem; font-family: var(--font-heading);">Kütüphane Yönetim Paneli</h1>
        <p class="text-secondary" style="font-size: 1rem;">Kitap envanterinizi, fiyatlandırma ve stok durumlarını buradan yönetebilirsiniz.</p>
      </div>
      <div>
        <router-link to="/ekle" class="premium-btn">
          <i class="bi bi-plus-lg"></i> Yeni Kitap Ekle
        </router-link>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row g-4 mb-5">
      <div class="col-md-6 col-xl-3">
        <div class="premium-card stat-card">
          <div class="stat-info">
            <span class="text-secondary fw-semibold uppercase" style="font-size: 0.85rem;">Toplam Kitap</span>
            <h3 class="mt-2 text-primary">{{ kitapSayisi }}</h3>
          </div>
          <div class="stat-icon-box">
            <i class="bi bi-journal-bookmark-fill"></i>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="premium-card stat-card">
          <div class="stat-info">
            <span class="text-secondary fw-semibold uppercase" style="font-size: 0.85rem;">Favori Kitaplar</span>
            <h3 class="mt-2 text-warning">{{ favoriSayisi }}</h3>
          </div>
          <div class="stat-icon-box" style="background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.2); color: var(--status-warning);">
            <i class="bi bi-star-fill"></i>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="premium-card stat-card">
          <div class="stat-info">
            <span class="text-secondary fw-semibold uppercase" style="font-size: 0.85rem;">Toplam Stok</span>
            <h3 class="mt-2 text-info">{{ toplamStok }}</h3>
          </div>
          <div class="stat-icon-box" style="background: rgba(14, 165, 233, 0.1); border-color: rgba(14, 165, 233, 0.2); color: var(--status-info);">
            <i class="bi bi-box-seam-fill"></i>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-xl-3">
        <div class="premium-card stat-card">
          <div class="stat-info">
            <span class="text-secondary fw-semibold uppercase" style="font-size: 0.85rem;">Envanter Değeri</span>
            <h3 class="mt-2 text-success">{{ toplamDeger.toLocaleString('tr-TR', { style: 'currency', currency: 'TRY' }) }}</h3>
          </div>
          <div class="stat-icon-box" style="background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.2); color: var(--status-success);">
            <i class="bi bi-currency-exchange"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Search & Advanced Filter Section -->
    <div class="premium-card mb-4">
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
        <!-- Search bar input -->
        <div class="d-flex align-items-center gap-2 flex-grow-1" style="max-width: 500px; position: relative;">
          <i class="bi bi-search text-muted" style="position: absolute; left: 16px;"></i>
          <input 
            v-model="searchQuery" 
            type="text" 
            class="premium-input" 
            placeholder="Kitap adı, yazar, stok kodu veya tedarikçi ara..." 
            style="padding-left: 45px;"
          />
        </div>

        <!-- Filter and View Actions -->
        <div class="d-flex flex-wrap align-items-center gap-2">
          <!-- Filters -->
          <div class="btn-group shadow-sm" role="group">
            <button 
              @click="activeFilter = 'all'" 
              class="btn btn-sm py-2 px-3"
              :class="activeFilter === 'all' ? 'btn-primary' : 'premium-btn-secondary border-0'"
            >Tümü</button>
            <button 
              @click="activeFilter = 'fav'" 
              class="btn btn-sm py-2 px-3"
              :class="activeFilter === 'fav' ? 'btn-warning text-dark' : 'premium-btn-secondary border-0'"
            >Favoriler</button>
            <button 
              @click="activeFilter = 'instock'" 
              class="btn btn-sm py-2 px-3"
              :class="activeFilter === 'instock' ? 'btn-success text-white' : 'premium-btn-secondary border-0'"
            >Stokta Olanlar</button>
            <button 
              @click="activeFilter = 'outstock'" 
              class="btn btn-sm py-2 px-3"
              :class="activeFilter === 'outstock' ? 'btn-danger text-white' : 'premium-btn-secondary border-0'"
            >Tükenenler</button>
          </div>

          <!-- Divider -->
          <div class="vr bg-secondary mx-1" style="height: 30px; opacity: 0.3;"></div>

          <!-- View Mode Toggle Buttons -->
          <div class="btn-group" role="group">
            <button 
              @click="viewMode = 'grid'" 
              class="btn btn-sm px-3" 
              :class="viewMode === 'grid' ? 'btn-primary' : 'premium-btn-secondary border-0'"
              title="Kılavuz Görünümü"
            >
              <i class="bi bi-grid-3x3-gap-fill"></i>
            </button>
            <button 
              @click="viewMode = 'table'" 
              class="btn btn-sm px-3" 
              :class="viewMode === 'table' ? 'btn-primary' : 'premium-btn-secondary border-0'"
              title="Tablo Görünümü"
            >
              <i class="bi bi-table"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- KitapListesi Bileşeni (Girdi/Çıktı mantığı aynen korundu, viewMode ve filter parametreleri eklendi) -->
    <KitapListesi 
      :kitaplar="filtrelenmisKitaplar" 
      :hata="hata" 
      :view-mode="viewMode"
      @favori-degisti="favoriDegistir" 
      @sil="sil"
    >
      <p style="color: rgba(255,255,255,0.4); font-size: 0.8em; margin: 0;"><i class="bi bi-fire text-warning me-1"></i> Bu kitap çok satanlar listesinde!</p>
    </KitapListesi>

    <!-- --- EĞİTİM BÖLÜMÜ (details etiketi ile varsayılan olarak kapalı/gizli yapıldı) --- -->
    <details class="dev-console my-5">
      <summary class="dev-console-header py-3 px-4 fw-semibold text-secondary style-summary d-flex align-items-center justify-content-between" style="cursor: pointer; user-select: none;">
        <span><i class="bi bi-terminal-fill me-2"></i> Geliştirici Kumandası & Test Alanı (Aç / Kapat)</span>
        <i class="bi bi-chevron-down"></i>
      </summary>
      
      <div class="card-body p-4 border-top border-secondary border-opacity-25" style="background: rgba(12, 14, 20, 0.9);">
        <h1 class="h3 mb-3 text-secondary" style="font-family: monospace; font-size: 1.25rem;">{{ baslik }}</h1>
        <p class="lead text-muted" style="font-family: monospace; font-size: 0.9rem;">{{ mesaj }}</p>
        
        <div class="d-flex flex-wrap gap-2 mb-4">
          <button @click="degistir" class="btn btn-outline-secondary btn-sm font-monospace">Tıkla ve Sayacı Arttır</button>
          <button @click="odaklan" class="btn btn-outline-info btn-sm font-monospace">Inputa Odaklan</button>
          <button @click="oyunuBaslat" :disabled="oyunDurumu.basliyor" class="btn btn-primary btn-sm font-monospace">
            Okuma Testini Başlat
          </button>
        </div>

        <div class="alert alert-secondary my-3 p-3 shadow-sm rounded-3 bg-dark border-secondary border-opacity-25 font-monospace text-light">
          <p class="mb-1 text-secondary">Şu anki sayı: <strong class="text-warning fs-5">{{ sayac }}</strong></p>
          <p v-if="sayac > 5" class="text-success mb-1 fw-bold">Sayı 5'i geçti, harikasın!</p>
          <p class="mb-0 text-muted">{{ sayacMesaji }}</p>
        </div>

        <div class="mb-4 col-md-4">
          <input type="text" ref="isimInputu" class="form-control bg-dark border-secondary text-light font-monospace" placeholder="Odaklanılacak metin...">
        </div>

        <div v-if="oyunDurumu.basliyor" class="alert alert-info my-3 p-4 shadow-sm bg-dark border-info text-info">
          <Zamanlayici @bitir="sonucuGoster" />
        </div>

        <teleport to="body">
          <div v-if="oyunDurumu.bitti" class="modal" style="display: flex; align-items: center; justify-content: center; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); z-index: 9999;">
            <div class="modal-dialog bg-dark p-4 rounded-4 shadow-lg border border-secondary border-opacity-50 text-light" style="max-width: 400px; width: 100%;">
              <Sonuc :skor="oyunDurumu.skor" />
              <button @click="oyunDurumu.bitti = false" class="premium-btn mt-3 w-100 shadow-sm">Kapat</button>
            </div>
          </div>
        </teleport>
      </div>
    </details>
  </div>
</template>

<style scoped>
.style-summary::-webkit-details-marker {
  display: none;
}
</style>
