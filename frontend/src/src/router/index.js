import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import MainPage from '../components/MainPage.vue'; // если вы его используете
import NewProjectPage from '../components/NewProjectPage.vue';

const routes = [
  { path: '/', component: LoginPage }, // Начальная страница - страница логина
  { path: '/login', component: LoginPage }, // Страница логина
  { path: '/register', component: RegisterPage }, // Страница регистрации
  { path: '/main', component: MainPage }, // Главная страница, если она нужна
  { path: '/new-project', component: NewProjectPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;