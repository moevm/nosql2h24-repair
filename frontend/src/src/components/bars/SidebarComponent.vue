<template>
  <aside class="sidebar">
    <div v-if="!isMainPage" class="menu-item" @click="goToMain">
      <img src="@/assets/icons/home.png" alt="Home Icon" class="icon">
      <p>На основную</p>
    </div>
    <div v-if="userRole === 'Администратор'" class="menu-item" @click="goToUsers">
      <img src="@/assets/icons/user.png" alt="User Icon" class="icon">
      <p>Пользователи</p>
    </div>
    <div v-if="!isMainPage && !isMessages && userRole !== 'Рабочий'" :class="['menu-item', { 'active': isPhasesPage }]" @click="goToPhases">
      <img src="@/assets/icons/phases.png" alt="Phases Icon" class="icon">
      <p>Этапы</p>
    </div>
    <div v-if="!isMainPage && !isMessages && userRole !== 'Рабочий'" :class="['menu-item', { 'active': isProcurementsPage }]" @click="goToProcurements">
      <img src="@/assets/icons/procurements.png" alt="Procurements Icon" class="icon">
      <p>Закупки</p>
    </div>
    <div v-if="!isMainPage && !isMessages && userRole !== 'Рабочий'" :class="['menu-item', { 'active': isRisksPage }]" @click="goToRisks">
      <img src="@/assets/icons/risks.png" alt="Risks Icon" class="icon">
      <p>Риски</p>
    </div>
    <div v-if="isMainPage && userRole === 'Заказчик'" class="menu-item" @click="goToStatistics">
      <img src="@/assets/icons/statics.png" alt="Static Icon" class="static-icon">
      <p>Статистика</p>
    </div>
    <div v-if="isMainPage && userRole === 'Администратор'" class="menu-item" @click="goToStatistics">
      <img src="@/assets/icons/statics.png" alt="Static Icon" class="static-icon">
      <p>Статистика</p>
    </div>
    <div class="menu-item logout-item" @click="logOut">
      <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
    </div>
  </aside>
</template>

<script>
import axios from 'axios';
import { clearAllCookies, useCookies } from '@/src/js/useCookies';
const { getProjectId } = useCookies();
const clearCookies = () => {
  clearAllCookies();
};

export default {
  data() {
    return {
      serverError: '', // Добавлено для хранения ошибок с сервера
    };
  },
  computed: {
    isMainPage() {
      return this.$route.path === '/main';
    },
    isMessages() {
      return (this.$route.path === '/messages' || this.$route.path === '/chat' || this.$route.path === '/add_contact' || this.$route.path === '/user-search' || this.$route.path === '/statistics' || this.$route.path === '/add_worker' || this.$route.path === '/add_new_worker' || this.$route.path === '/new-project');
    },
    isPhasesPage() {
      return this.$route.path === '/stages';
    },
    isProcurementsPage() {
      return this.$route.path === '/procurements';
    },
    isRisksPage() {
      return this.$route.path === '/risks';
    },
    userRole() {
      const user = this.$store.getters.getUser[0];
      return user ? user.role : null;
    },
  },
  methods: {
    goToMain() {
      this.$router.push('/main');
    },
    goToPhases() {
      if (this.$route.fullPath === `/stages`) {
        this.$router.push(`/project/${getProjectId()}`);
      } else {
        this.$router.push(`/stages`);
      }
    },
    goToProcurements() {
      if (this.$route.fullPath === `/procurements`) {
        this.$router.push(`/project/${getProjectId()}`);
      } else {
        this.$router.push(`/procurements`);
      }
    },
    goToRisks() {
      if (this.$route.fullPath === `/risks`) {
        this.$router.push(`/project/${getProjectId()}`);
      } else {
        this.$router.push(`/risks`);
      }
    },
    goToStatistics() {
      this.$router.push('/statistics');
    },
    goToUsers() {
      this.$router.push('/user-search');
    },
    async logOut() {
      try {
        const res = await axios.post('/api/auth/logout');
        console.log(res);
        clearCookies();
        this.$store.commit('removeUsers');  // Изменяем состояние
        this.$router.push('/login');
      } catch (error) {
        if (error.response.status === 401) {
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          if (error.response.data.detail) {
            this.serverError = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }
    }
  }
};
</script>

<style scoped>
.sidebar {
  width: 100px;
  height: 90vh;
  position: fixed;
  top: 60px;
  left: 0;
  background-color: #f4f4f4;
  padding: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.menu-item {
  cursor: pointer;
  padding: 10px 0;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.icon,
.static-icon,
.logout-icon {
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
}

.menu-item p {
  margin: 0;
  font-size: 16px;
}

.logout-item {
  margin-top: auto;
}

.active {
  position: relative;
}

.active::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90px;
  height: 90px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  z-index: -1;
}
</style>
