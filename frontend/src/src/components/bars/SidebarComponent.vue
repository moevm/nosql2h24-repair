<template>
    <aside class="sidebar">
      <button v-if="!isMainPage" @click="goToMain" class="to-main-button">На основную</button>
      <div class="menu-item" @click="logOut">
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
    computed: {
      isMainPage() {
        return this.$route.path === '/main';
      },
    },
    methods: {
      goToMain() {
        this.$router.push('/main');
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
    display: flex;
    flex-direction: column;
    height: 90vh;
    width: 100px;
    position: fixed;
    top: 60px;
    left: 0;
    background-color: #f4f4f4;
    padding: 20px;
    text-align: center;
  }
  
  .menu-item {
    cursor: pointer;
    margin-top: auto;
    padding: 10px 0;
    font-size: 16px;
    flex-direction: column; /* Размещает элементы в столбец */
    cursor: pointer;
  }

  .logout-item {
    text-align: center;
    margin-top: auto; /* Перемещает элемент вниз */
  }
  </style>
