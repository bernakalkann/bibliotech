import { ref, onMounted } from 'vue';
import axios from 'axios';

export function useKitaplar() {
  const kitaplar = ref([]);
  const hata = ref(null);

  const kitaplariGetir = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/kitaplar/');
      kitaplar.value = res.data;
    } catch (err) {
      hata.value = 'Kitaplar yüklenemedi!';
    }
  };

  const kitapEkle = async (yeniKitap) => {
    try {
      await axios.post('http://127.0.0.1:8000/api/kitaplar/', yeniKitap, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` }
      });
      await kitaplariGetir();
    } catch (err) {
      hata.value = err.response ? JSON.stringify(err.response.data) : 'Kitap eklenemedi!';
    }
  };

  const kitapSil = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/kitaplar/${id}/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access')}` }
      });
      await kitaplariGetir();
    } catch (err) {
      hata.value = 'Silme işlemi başarısız!';
    }
  };

  onMounted(kitaplariGetir);
  return { kitaplar, hata, kitapEkle, kitapSil };
}