import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import KitapEkle from '../views/KitapEkle.vue'
import GirisYap from '../views/GirisYap.vue';

const routes = [
  { path: '/giris', component: GirisYap },
  { 
  path: '/duzenle/:id', 
  name: 'KitapDuzenle', 
  component: () => import('../views/KitapDuzenle.vue') 
  },
  { path: '/', name: 'home', component: HomeView },
  { 
    path: '/hakkimizda', 
    name: 'about', 
    component: () => import('../views/AboutView.vue') 
  },
  {
    path: '/ekle',
    name: 'KitapEkle',
    component: KitapEkle
  },
  { 
    path: '/kitap/:id', 
    name: 'KitapDetay', 
    component: () => import('../views/KitapDetayView.vue') 
  }, // <--- BURAYA VİRGÜL KOYDUK!
  { path: '/hakkimizdad', redirect: '/hakkimizda' },
  { path: '/:catchAll(.*)', name: 'NotFound', component: () => import('../views/NotFoundView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router