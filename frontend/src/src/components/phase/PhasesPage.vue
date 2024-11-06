<template>
    <div class="phases-page">
      <HeaderComponent />
      <ProjectSidebarComponent />
      <main class="content">
        <h1>Этапы проекта</h1>
        <!-- Добавьте сюда содержимое для этапов проекта -->
      </main>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../bars/HeaderComponent.vue';
  import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
  
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