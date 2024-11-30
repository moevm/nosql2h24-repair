<template>
    <HeaderComponent />
    <ProjectSidebarComponent :projectId="projectId" :projectName="nameProject"/>
    <div class="form-container">
      <h2>{{ taskId ? 'Редактировать риск' : 'Новая карточка риска' }}</h2>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="title">Название</label>
          <input type="text" id="title" v-model="name" required />
        </div>
  
        <div class="form-group">
          <label for="description">Описание</label>
          <textarea id="description" v-model="description" required></textarea>
        </div>
        
        <button type="submit">Сохранить</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../bars/HeaderComponent.vue';
  import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
  import axios from 'axios';
  import {clearAllCookies, useCookies} from '@/src/js/useCookies';
  const { getProjectId } = useCookies();
  export default {
    components: {
        HeaderComponent,
        ProjectSidebarComponent,
    },
    data() {
      return {
        name: '',
        description: '',
        errorMessage: '',
        showErrors: false,
      };
    },
    methods: {
      async submitForm() {
        this.showErrors = true;
          const dataToSend = {
            name: this.name,
            description: this.description,
          };
          try {
            const res = await axios.post(`/api/projects/${getProjectId()}/add_risk`, dataToSend, {
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            console.log(res);
            alert('Риск успешно создан!');
            this.$router.push(`/risks`);
          } catch (error) {
            if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            console.error("Ошибка сети:", error.message);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }

        }

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
    background-color: #625b71;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>   