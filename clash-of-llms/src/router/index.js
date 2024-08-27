import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import NetworkGraph from '../components/NetworkGraph.vue';  // Import the NetworkGraph component

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
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
