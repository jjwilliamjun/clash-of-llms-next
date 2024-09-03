import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import NetworkGraph from '../components/NetworkGraph.vue';  // Import the NetworkGraph component
import ParameterView from '@/components/ParameterView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
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
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
