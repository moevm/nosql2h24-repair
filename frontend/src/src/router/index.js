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
  { path: '/:projectName/:id', component: ProjectPage},
  { path: '/:projectName/:id/stages', component: StagesPage},
  { path: '/:projectName/:id/risks', component: RisksPage},
  { path: '/:projectName/:id/procurements', component: ProcurementsPage},
  { path: '/messages', component: MessagesPage},
  { path: '/chat/:userId', component: ChatPage},
  { path: '/:projectName/:id/risks/add_risk', component: RiskFormComponent },
  { path: '/:projectName/:id/risk-details/:taskId', component: RiskDetails},
  { path: '/material/:id', component: MaterialDetail},
  { path: '/:projectName/:id/procurements/add_procurement', component: MaterialEditAdd},
  // { path: '/add-material', component: MaterialEditAdd},
  { path: '/:projectName/:id/:stageName/:stageId/tasks/', component: TasksListPage, props: true},
  { path: '/tasks/:stageId/:taskId', component: TaskPage, props: true},
  { path: '/:projectName/:id/add-stage', name: 'add-stage', component: AddStagePage },
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
});

export default router;
