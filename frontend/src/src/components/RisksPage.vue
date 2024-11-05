<template>
    <div class="risks-page">
      <HeaderComponent />
      <ProjectSidebarComponent />
      <main class="content">
        <h1>Риски проекта</h1>
        <!-- Добавьте сюда содержимое для рисков проекта -->
      </main>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../components/HeaderComponent.vue';
  import ProjectSidebarComponent from '../components/ProjectSidebarComponent.vue';
  
  export default {
    components: {
      HeaderComponent,
      ProjectSidebarComponent,
    },
  };
  </script>
  
  <style scoped>
  .content {
    margin-left: 150px;
    padding-top: 60px; /* Увеличиваем отступ сверху, чтобы учесть фиксированный заголовок и поле поиска */
  }
  </style>  