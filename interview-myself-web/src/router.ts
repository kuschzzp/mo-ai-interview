import { createRouter, createWebHistory } from 'vue-router';

const Home = () => import('./pages/Home.vue');
const Interview = () => import('./pages/Interview.vue');

export const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/', name: 'home', component: Home },
		{ path: '/interview', name: 'interview', component: Interview },
		{ path: '/:pathMatch(.*)*', redirect: '/' },
	],
});


