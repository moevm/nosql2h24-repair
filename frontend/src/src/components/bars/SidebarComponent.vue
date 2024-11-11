<template>
    <aside class="sidebar">
      <div class="menu-item" @click="logOut">
        <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
      </div>
    </aside>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    methods: {
      async logOut() {
        // Логика выхода на страницу авторизации
        try {
          const res = await axios.post('/api/auth/logout');
          console.log(res);
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
    height: 100vh;
    position: fixed;
    top: 60px;
    left: 0;
    background-color: #f4f4f4;
    padding: 20px;
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

  .logout-item {
    margin-top: auto; /* Перемещает элемент вниз */
  }
  </style>  
