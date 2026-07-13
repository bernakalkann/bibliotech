# Bibliotech - Premium Kitap Yönetim Sistemi

Bibliotech; modern web standartlarında tasarlanmış, **Django REST Framework (Backend)** ve **Vue 3 (Frontend)** teknolojilerini bir araya getiren estetik ve yüksek performanslı bir kütüphane yönetim panelidir.

Uygulama; cam efekti tasarımı (glassmorphism), detaylı istatistik grafikleri, gelişmiş arama/filtreleme motoru, çoklu görünüm desteği (Tablo/Grid), kullanıcı yetkilendirmesi ve şık toast bildirimleriyle donatılmıştır.

---

## Ekran Görüntüleri (Arayüz Sunumu)

<p align="center">
  <b>Ana Kontrol Paneli (Dashboard) ve Grid Görünümü</b><br/>
  <i>Kütüphane envanteri, toplam stok değerleri ve favori kitap istatistiklerinin dinamik olarak sergilendiği ana arayüz.</i><br/><br/>
  <img src="ekran_resimleri/Ekran%20Resmi%202026-07-13%2014.27.42.png" width="100%" alt="Bibliotech Dashboard" />
</p>

<br/>

<table width="100%">
  <tr>
    <td width="50%" align="center" valign="top">
      <b>Tablo Görünümü ve Sıralama</b><br/>
      <i>Envanterin detaylı listelendiği ve anlık sıralandığı mod.</i><br/><br/>
      <img src="ekran_resimleri/Ekran%20Resmi%202026-07-13%2014.27.49.png" width="100%" alt="Tablo Listesi" />
    </td>
    <td width="50%" align="center" valign="top">
      <b>Kitap Detay Kartı</b><br/>
      <i>Kitap bilgilerinin 3D kapak eşliğinde sunulduğu profil ekranı.</i><br/><br/>
      <img src="ekran_resimleri/Ekran%20Resmi%202026-07-13%2014.28.03.png" width="100%" alt="Kitap Detay" />
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <br/><b>Yeni Kitap Ekleme Formu</b><br/>
      <i>Dinamik stok seviyesi uyarısı içeren kitap ekleme formu.</i><br/><br/>
      <img src="ekran_resimleri/Ekran%20Resmi%202026-07-13%2014.27.58.png" width="100%" alt="Kitap Ekle" />
    </td>
    <td width="50%" align="center" valign="top">
      <br/><b>Glassmorphism Sistem Girişi</b><br/>
      <i>Cam efekti ve neon detaylı modern giriş paneli.</i><br/><br/>
      <img src="ekran_resimleri/Ekran%20Resmi%202026-07-13%2014.28.22.png" width="100%" alt="Giriş Ekranı" />
    </td>
  </tr>
</table>

---

## Django Backend & API Mimarisi

Uygulamanın veri yönetimi ve güvenlik altyapısı Python tabanlı **Django REST Framework (DRF)** kullanılarak kurgulanmıştır.

### 1. Veri Modeli Şeması (Kitap Modeli)
Veritabanında kayıtlı kitapların yapısı şu alanları (fields) içerir:
*   `baslik` (CharField, max: 200) - Kitabın başlığı.
*   `yazar` (CharField, max: 100) - Kitabın yazarı.
*   `fav` (BooleanField, default: False) - Favori durumu.
*   `sku` (CharField, max: 50, opsiyonel) - Eşsiz Stok Kodu.
*   `fiyat` (FloatField) - Birim satış fiyatı.
*   `adet` (IntegerField) - Mevcut stok adedi.
*   `tedarikci` (CharField, max: 100) - Kitabı sağlayan tedarikçi yayınevi/firma.

### 2. API Uç Noktaları (API Endpoints)
Tüm servis istekleri `http://localhost:8000/api/` kök URL yapısı altından sunulur:

| Metot | API Adresi | Erişim Yetkisi | Açıklama |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/kitaplar/` | Herkese Açık | Tüm kitapların listesini döndürür. |
| **POST** | `/api/kitaplar/` | **Giriş Şart** | Envantere yeni kitap ekler. |
| **GET** | `/api/kitaplar/<id>/` | Herkese Açık | Belirtilen ID'ye sahip kitabın detayını döndürür. |
| **PUT** | `/api/kitaplar/<id>/` | **Giriş Şart** | Kitap verilerini günceller (fiyat, stok, favori vb.). |
| **DELETE**| `/api/kitaplar/<id>/` | **Giriş Şart** | Kitabı veritabanından tamamen siler. |
| **POST** | `/api/token/` | Herkese Açık | Kullanıcı adı ve şifreyle **JWT Access & Refresh Token** üretir. |
| **POST** | `/api/token/refresh/`| Herkese Açık | Mevcut refresh token ile yeni access token üretir. |

### 3. JWT Tabanlı Yetkilendirme (SimpleJWT)
Ekleme, güncelleme ve silme (CORS write) işlemleri için REST API, `IsAuthenticatedOrReadOnly` izniyle korunur. Giriş yapıldığında üretilen JWT Bearer token bilgileri HTTP başlıklarında (`Authorization: Bearer <token>`) taşınarak istekler doğrulanır.

### 4. Yönetim Paneli (Django Admin)
Sistem yöneticileri için `/admin/` adresi altında Django'nun dahili yönetim paneli aktiftir. `Kitap` modeli yönetim paneline kaydedilmiş olup, arayüzden bağımsız olarak veritabanı kayıtlarının manuel yönetimine olanak tanır.

---

## Özellikler (Features)

*   **Premium Glassmorphism Arayüz:** Modern neon renk geçişleri ve yarı saydam cam katmanları.
*   **Çift Görünüm Desteği:** Tablo (Enterprise) ve Grid (Library) görünümleri arasında anlık geçiş.
*   **Gelişmiş Arama ve Filtreleme:** Başlık, yazar, SKU ve tedarikçiye göre arama yapabilme; favorilere, stok durumlarına göre anlık filtreleme.
*   **İstatistik Paneli:** Toplam kitap sayısı, toplam stok, favoriler ve toplam envanter maliyeti hesaplama.
*   **Kullanıcı Kimlik Doğrulama:** JWT (SimpleJWT) tabanlı güvenli giriş sistemi.
*   **Toast Bildirim Sistemi:** Başarılı, hatalı veya uyarı durumlarında ekran köşesinde beliren animasyonlu bildirimler.
*   **Karanlık / Açık Tema:** Göz yormayan karanlık tema ve şık açık tema desteği.

---

## Teknoloji Yığını (Tech Stack)

### **Backend (Sunucu)**
*   **Python 3** & **Django 6**
*   **Django REST Framework** (RESTful API uç noktaları için)
*   **django-cors-headers** (CORS güvenliği yapılandırması)
*   **djangorestframework-simplejwt** (JWT Kimlik Doğrulama token sistemi)
*   **SQLite** (Geliştirme veritabanı)

### **Frontend (Arayüz)**
*   **Vue 3 (Composition API)**
*   **Vue Router** (Sayfa yönlendirmeleri için)
*   **Axios** (Backend ile HTTP istekleri)
*   **Bootstrap 5** & **Bootstrap Icons** (Temel yerleşim ve ikonlar)
*   **Plus Jakarta Sans** & **Playfair Display** (Özel Google Fonts tipografisi)

---

## Kurulum ve Çalıştırma

Projenin yerel bilgisayarınızda çalıştırılması için aşağıdaki adımları uygulayın:

### 1. Backend (Django) Çalıştırma
```bash
# 1. Projenin backend klasörüne gidin:
cd backend

# 2. Python sanal ortamını aktif edin:
source ~/.local/share/virtualenvs/kitap-projesi-0KrOaeLp/bin/activate

# 3. Veritabanı sunucusunu başlatın:
python manage.py runserver
```

### 2. Frontend (Vue 3) Çalıştırma
```bash
# 1. Projenin frontend klasörüne gidin:
cd frontend

# 2. Gerekli NPM paketlerini yükleyin:
npm install

# 3. Sunucuyu ayağa kaldırın:
npm run dev
```

---

## Proje Dizin Yapısı

```text
├── backend/                 # Django Backend Projesi
│   ├── kitap_app/           # Kitap Modeli ve API Görünümleri
│   ├── myproject/           # Proje Ayarları (settings.py, urls.py)
│   └── db.sqlite3           # SQLite Veritabanı
├── frontend/                # Vue.js Frontend Projesi
│   ├── src/
│   │   ├── components/      # Kitap Listesi ve Küçük Bileşenler
│   │   ├── views/           # Sayfa Görünümleri (Home, Add, Edit, Detail, Auth)
│   │   ├── composables/     # API İsteklerini Yöneten Composable Dosyaları
│   │   ├── router/          # Yönlendirme Ayarları
│   │   ├── App.vue          # Ana Dashboard Shell Yapısı
│   │   └── style.css        # Premium Tasarım Sistemi & CSS Değişkenleri
│   └── index.html           # Ana HTML Sayfası
└── ekran_resimleri/         # Arayüze Ait Ekran Görüntüleri
```
