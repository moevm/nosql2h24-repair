<template>
  <aside class="sidebar">
    <button v-if="!isMainPage" @click="goToMain" class="to-main-button">На основную</button>
    <div class="menu-item" @click="goToPhases">
      <img src="@/assets/icons/phases.png" alt="Phases Icon" class="icon">
      <p>Этапы</p>
    </div>
    <div class="menu-item" @click="goToProcurements">
      <img src="@/assets/icons/procurements.png" alt="Procurements Icon" class="icon">
      <p>Закупки</p>
    </div>
    <div class="menu-item" @click="goToRisks">
      <img src="@/assets/icons/risks.png" alt="Risks Icon" class="icon">
      <p>Риски</p>
    </div>
    <div class="menu-item logout-item" @click="logOut">
      <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
    </div>
  </aside>
</template>

<script>
import { clearAllCookies } from '@/src/js/useCookies';
const clearCookies = () => {
  clearAllCookies();
};
import axios from 'axios';

export default {
  props: {
  },
  computed: {
    isMainPage() {
      return this.$route.path === '/main';
    },
  },
  methods: {
    goToPhases() {
      if (this.$route.fullPath === `/stages`){
        this.$router.push(`/project`);
      } else {
        // Логика перехода на страницу этапов
        this.$router.push(`/stages`);
      }
    },
    goToMain() {
      this.$router.push('/main');
    },
    goToRisks() {
      if (this.$route.fullPath === `/risks`){
        this.$router.push(`/project`);
      } else {
        // Логика перехода на страницу рисков
        this.$router.push(`/risks`);
      }
    },
    goToProcurements() {
      if (this.$route.fullPath === `/procurements`){
        this.$router.push(`/project`);
      } else {
        // Логика перехода на страницу закупок
        this.$router.push(`/procurements`);
      }
    },
    async logOut() {
      // Логика выхода на страницу авторизации
      try {
        const res = await axios.post('/api/auth/logout');
        console.log(res);
        clearCookies();
        this.$router.push('/login');
        // Дополнительный код для обработки успешной регистрации
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
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
  flex-direction: column;
  top: 60px;
  left: 0;
  background-color: #f4f4f4;
  padding: 20px;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
}

.menu-item {
  cursor: pointer;
  padding: 10px 0;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column; /* Размещает элементы в столбец */
  align-items: center; /* Центрирует элементы по горизонтали */
  cursor: pointer;
}

.icon {
  width: 50px; /* Задайте нужный размер иконки */
  height: 50px; /* Задайте нужный размер иконки */
  margin-bottom: 10px; /* Отступ между иконкой и текстом */
}

.menu-item p {
  margin: 0; /* Убираем отступы у текста */
  font-size: 16px; /* Задайте нужный размер текста */
}

.logout-item {
  margin-top: auto; /* Перемещает элемент вниз */
}
</style>
