import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import NetworkGraph from '../components/NetworkGraph.vue';
import GamePlay from '@/components/GamePlay.vue';
import FileUpload from '@/components/FileUpload.vue';
import PreviewSettings from '@/components/PreviewSettings.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/network',
    name: 'network',
    component: NetworkGraph,
  },
  {
    path: '/gameplay',
    name: 'gameplay',
    component: GamePlay,
  },
  {
    path: '/upload',
    name: 'upload',
    component: FileUpload,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },
  {
    path: '/preview',
    name: 'preview',
    component: PreviewSettings
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
