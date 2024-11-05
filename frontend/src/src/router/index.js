import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import MainPage from '../components/MainPage.vue'; // если вы его используете
import NewProjectPage from '../components/NewProjectPage.vue';
import ProjectPage from '../components/ProjectPage.vue';
import PhasesPage from '../components/PhasesPage.vue';
import RisksPage from '../components/RisksPage.vue';
import ProcurementsPage from '../components/ProcurementsPage.vue';
import MessagesPage from '../components/MessagesPage.vue';
import ChatPage from '../components/ChatPage.vue';


const routes = [
  { path: '/', component: LoginPage }, // Начальная страница - страница логина
  { path: '/login', component: LoginPage }, // Страница логина
  { path: '/register', component: RegisterPage }, // Страница регистрации
  { path: '/main', component: MainPage }, // Главная страница, если она нужна
  { path: '/new-project', component: NewProjectPage},
  { path: '/project/:id', component: ProjectPage},
  { path: '/project/phases', component: PhasesPage},
  { path: '/project/risks', component: RisksPage},
  { path: '/project/procurements', component: ProcurementsPage},
  { path: '/messages', component: MessagesPage},
  { path: '/chat/:userId', component: ChatPage},
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
});

export default router;