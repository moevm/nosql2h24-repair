<template>
    <aside class="sidebar">
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
      <div class="menu-item" @click="logOut">
        <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
      </div>
    </aside>
  </template>
  
  <script>
  export default {
    props: {
      projectId:{
        type: String,
        required: true,
      },
      projectName: {
        type: String,
        required: true,
      },
    },
    methods: {
      goToPhases() {
        // Логика перехода на страницу этапов
        this.$router.push(`/${this.projectName}/${this.projectId}/stages`);
      },
      goToRisks() {
        // Логика перехода на страницу рисков
        this.$router.push(`/${this.projectName}/${this.projectId}/risks`);
      },
      goToProcurements() {
        // Логика перехода на страницу закупок
        this.$router.push(`/${this.projectName}/${this.projectId}/procurements`);
      },
      logOut() {
        // Логика выхода на страницу авторизации
        this.$router.push('/login');
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
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
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
  </style>  
