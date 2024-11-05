<template>
    <HeaderComponent />
    <SidebarComponent />
    <div class="create-project-page">
      <h1>Опишите проект</h1>
      <textarea v-model="projectDescription" placeholder="Введите описание проекта"></textarea>
      <button @click="submitProject">Отправить</button>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../components/HeaderComponent.vue';
  import SidebarComponent from '../components/SidebarComponent.vue';
  export default {
    components: {
      HeaderComponent,
      SidebarComponent
    },
    data() {
      return {
        projectDescription: '',
      };
    },
    methods: {
      submitProject() {
        // Логика отправки проекта
        console.log('Project Description:', this.projectDescription);
        // Здесь можно добавить логику для отправки данных на сервер
      },
    },
  };
  </script>
  
  <style scoped>
  .create-project-page {
    display: flex;
    flex-direction: column;
    padding: 20px;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  textarea {
    width: 100%;
    height: 200px;
    margin-bottom: 20px;
    padding: 10px;
    font-size: 16px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button:hover {
    background-color: #0056b3;
  }

  .create-project-page {
  margin-left: 200px;
  padding-top: 80px;
}
  </style>  