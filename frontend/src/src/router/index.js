import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/auth_reg/LoginPage.vue';
import RegisterPage from '../components/auth_reg/RegisterPage.vue';
import MainPage from '../components/MainPage.vue';
import NewProjectPage from '../components/project/NewProjectPage.vue';
import ProjectPage from '../components/project/ProjectPage.vue';
import StagesPage from '../components/stage/StagesPage.vue';
import RisksPage from '../components/risk/RisksPage.vue';
import ProcurementsPage from '../components/material/ProcurementsPage.vue';
import MessagesPage from '../components/message/MessagesPage.vue';
import ChatPage from '../components/message/ChatPage.vue';
import RiskFormComponent from '../components/risk/RiskFormComponent.vue';
import RiskDetails from '../components/risk/RiskDetails.vue';
import MaterialDetail from '../components/material/MaterialDetail.vue';
import MaterialEditAdd from '../components/material/MaterialEditAdd.vue';
import TasksListPage from '../components/task/TasksListPage.vue';
import TaskPage from '../components/task/TaskPage.vue';
import AddStagePage from '../components/stage/AddStagePage.vue';


const routes = [
  { path: '/', component: LoginPage }, // Начальная страница - страница логина
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/main', component: MainPage },
  { path: '/new-project', component: NewProjectPage},
  { path: '/project/:id', component: ProjectPage},
  { path: '/project/stages', component: StagesPage},
  { path: '/project/risks', component: RisksPage},
  { path: '/project/procurements', component: ProcurementsPage},
  { path: '/messages', component: MessagesPage},
  { path: '/chat/:userId', component: ChatPage},
  { path: '/add-risk', component: RiskFormComponent },
  { path: '/risk-details/:taskId', component: RiskDetails},
  { path: '/material/:id', component: MaterialDetail},
  { path: '/material/edit/:id', component: MaterialEditAdd},
  { path: '/add-material', component: MaterialEditAdd},
  { path: '/tasks/:stageId', component: TasksListPage},
  { path: '/tasks/:stageId/:taskId', component: TaskPage},
  { path: '/add-stage', name: 'add-stage', component: AddStagePage },
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
});

export default router;
