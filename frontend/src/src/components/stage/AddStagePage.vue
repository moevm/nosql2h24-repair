<template>
    <div class="add-stage-page">
      <HeaderComponent />
      <ProjectSidebarComponent />
      <div class="main-content">
        <div class="add-stage-container">
          <h2>Добавить этап</h2>
  
          <div class="add-stage-form">
            <input
              v-model="newStageName"
              type="text"
              placeholder="Название нового этапа"
              class="stage-name-input"
            />
            <input
              v-model="newStageStartDate"
              type="date"
              class="stage-date-input"
            />
            <input
              v-model="newStageEndDate"
              type="date"
              class="stage-date-input"
            />
            <button @click="addStage">Добавить этап</button>
          </div>
        </div>
      </div>
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
    data() {
      return {
        newStageName: '',
        newStageStartDate: '',
        newStageEndDate: '',
      };
    },
    methods: {
      addStage() {
        if (this.newStageName && this.newStageStartDate && this.newStageEndDate) {
          const newStage = {
            id: Date.now(), // Используем текущее время для уникальности
            name: this.newStageName,
            startDate: this.newStageStartDate,
            endDate: this.newStageEndDate,
          };
          
          // Этап добавляется в родительский компонент
          this.$router.push({ name: 'stages' }); // Возвращаемся на страницу этапов
          this.$emit('add-stage', newStage); // Отправляем событие в родительский компонент
        } else {
          alert('Пожалуйста, заполните все поля.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .add-stage-page {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  .main-content {
    display: flex;
    margin-left: 150px;
    padding-top: 60px;
    width: calc(100% - 150px);
  }
  .add-stage-container {
    flex: 1;
    padding: 16px;
  }
  .add-stage-form {
    display: flex;
    flex-direction: column;
    margin-bottom: 16px;
  }
  .add-stage-form input {
    margin-bottom: 8px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .add-stage-form button {
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .add-stage-form button:hover {
    background-color: #45a049;
  }
  </style>  