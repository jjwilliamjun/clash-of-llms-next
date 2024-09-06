import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import NetworkGraph from '../components/NetworkGraph.vue';
import ParameterView from '@/components/ParameterView.vue';
import FileUpload from '@/components/FileUpload.vue';

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
    path: '/parameters',
    name: 'parameters',
    component: ParameterView,
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
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
