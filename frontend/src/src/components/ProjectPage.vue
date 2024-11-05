<template>
    <div class="project-page">
      <HeaderComponent />
      <ProjectSidebarComponent />
      <main class="content">
        <div class="project-header">
          <h1>{{ projectName }}</h1>
          <p>Местоположение: {{ projectLocation }}</p>
          <p>Дата начала: {{ startDate }}</p>
          <p>Дата окончания: {{ endDate }}</p>
          <p>Фаза проекта: {{ projectPhase }}</p>
          <p>Статус проекта: {{ projectStatus }}</p>
        </div>
        <div class="project-details">
          <!-- Добавьте сюда дополнительные детали проекта -->
        </div>
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
    data() {
      return {
        projectName: '',
        projectLocation: '',
        startDate: '',
        endDate: '',
        projectPhase: '',
        projectStatus: '',
      };
    },
    created() {
      // Предположим, что данные проекта передаются через параметры маршрута
      const project = this.$route.params.project;
      if (project) {
        this.projectName = project.name;
        this.projectLocation = project.location;
        this.startDate = project.startDate;
        this.endDate = project.endDate;
        this.projectPhase = project.phase;
        this.projectStatus = project.status;
      }
    },
  };
  </script>
  
  <style scoped>
  .content {
    margin-left: 150px;
    padding-top: 60px; /* Увеличиваем отступ сверху, чтобы учесть фиксированный заголовок и поле поиска */
  }
  
  .project-header {
    background-color: #fff;
    padding: 20px;
    border-bottom: 1px solid #ccc;
  }
  
  .project-details {
    padding: 20px;
  }
  </style>  