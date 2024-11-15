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
import UserSearchPage from '../components/message/UserSearchPage.vue';
import AddTaskPage from '../components/task/TaskAddPage.vue';
import AddContactPage from "@/src/components/message/AddContactPage.vue";

const routes = [
  { path: '/', component: LoginPage }, // Начальная страница - страница логина
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/main', component: MainPage },
  { path: '/new-project', component: NewProjectPage},
  { path: '/project', component: ProjectPage},
  { path: '/stages', component: StagesPage},
  { path: '/risks', component: RisksPage},
  { path: '/procurements', component: ProcurementsPage},
  { path: '/messages', component: MessagesPage},
  { path: '/chat', component: ChatPage},
  { path: '/add_risk', component: RiskFormComponent },
  { path: '/risk-details/', component: RiskDetails},
  { path: '/material/:id', component: MaterialDetail},
  { path: '/add_procurement', component: MaterialEditAdd},
  { path: '/add_task', component: AddTaskPage},
  { path: '/add_contact', component: AddContactPage},
  // { path: '/add-material', component: MaterialEditAdd},
  { path: '/tasks', component: TasksListPage, props: true},
  { path: '/tasks/viewRedactorTask', component: TaskPage, props: true},
  { path: '/add-stage', name: 'add-stage', component: AddStagePage },
  { path: '/user-search', component: UserSearchPage },
];

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
});

export default router;
