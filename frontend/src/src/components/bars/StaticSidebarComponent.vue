<template>
    <aside class="sidebar">
      <div v-if="isCustomer" class="menu-item" @click="goToStatistics">
        <img src="@/assets/icons/statics.png" alt="Static Icon" class="static-icon">
        <p>Статистика</p>
      </div>
      <div class="menu-item" @click="logOut">
        <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
      </div>
    </aside>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        isCustomer: true, // Условие для отображения раздела статистики для заказчика
      };
    },
    methods: {
      goToStatistics() {
        // Логика перехода на страницу статистики
        this.$router.push('/statistics');
      },
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
  
  .static-icon {
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
