import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue'; // если вы его используете

const routes = [
  { path: '/', component: LoginPage }, // Начальная страница - страница логина
  { path: '/login', component: LoginPage }, // Страница логина
  { path: '/register', component: RegisterPage }, // Страница регистрации
  { path: '/home', component: HomePage }, // Главная страница, если она нужна
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;