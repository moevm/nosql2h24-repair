<template>
    <HeaderComponent />
    <ProjectSidebarComponent />
    <div class="form-container">
      <h2>{{ taskId ? 'Редактировать риск' : 'Новая карточка риска' }}</h2>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="title">Название</label>
          <input type="text" id="title" v-model="title" required />
        </div>
  
        <div class="form-group">
          <label for="description">Описание</label>
          <textarea id="description" v-model="description" required></textarea>
        </div>
        
        <button type="submit">Сохранить</button>
      </form>
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
    props: {
      taskId: {
        type: Number,
        default: null,
      },
    },
    data() {
      return {
        title: '',
        description: '',
      };
    },
    created() {
      // Если taskId передан, находим задачу и заполняем форму данными
      if (this.taskId) {
        const task = this.$root.$data.tasks.find(task => task.id === this.taskId);
        if (task) {
          this.title = task.title;
          this.description = task.description;
        }
      }
    },
    methods: {
      submitForm() {
        const task = {
          id: this.taskId || Date.now(),
          title: this.title,
          description: this.description,
        };
        this.$emit(this.taskId ? 'update-task' : 'add-task', task);
        this.$router.push('/project/risks');
      },
    },
  };
  </script>
  
  <style scoped>
  .form-container {
    padding: 20px;
    margin-left: 150px;
    padding-top: 60px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  button {
    padding: 5px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>   