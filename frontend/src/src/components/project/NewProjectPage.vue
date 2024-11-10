<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="create-project-page">
    <h1>Опишите проект</h1>
    <input v-model="projectName" type="text" placeholder="Введите название проекта" />
    <input v-model="startDate" type="date" placeholder="Дата начала" />
    <input v-model="endDate" type="date" placeholder="Дата окончания" />
    <textarea v-model="projectDescription" placeholder="Введите описание проекта"></textarea>
    <button @click="submitProject">Отправить</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';

export default {
  components: {
    HeaderComponent,
    SidebarComponent
  },
  data() {
    return {
      projectName: '',
      startDate: '',
      endDate: '',
      projectDescription: '',
      errorMessage: ''
    };
  },
  methods: {
    submitProject() {
      // Проверка, чтобы все поля были заполнены
      if (!this.projectName || !this.startDate || !this.endDate || !this.projectDescription) {
        this.errorMessage = 'Пожалуйста, заполните все поля';
        return;
      }
      // Логика отправки проекта
      console.log('Название проекта:', this.projectName);
      console.log('Дата начала:', this.startDate);
      console.log('Дата окончания:', this.endDate);
      console.log('Описание проекта:', this.projectDescription);

      // Здесь можно добавить логику для отправки данных на сервер
      this.errorMessage = ''; // Очистка ошибки, если все поля заполнены
    },
  },
};
</script>

<style scoped>
.create-project-page {
  display: flex;
  flex-direction: column;
  padding: 20px;
  margin-left: 200px;
  padding-top: 80px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

input[type="text"], input[type="date"], textarea {
  width: 100%;
  margin-bottom: 20px;
  padding: 10px;
  font-size: 16px;
}

textarea {
  height: 200px;
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

.error {
  color: red;
  margin-top: 10px;
}
</style>
