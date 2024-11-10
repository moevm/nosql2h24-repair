<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="create-project-page">
    <h1>Опишите проект</h1>
    <input v-model="projectName" type="text" placeholder="Введите название проекта" />
    <p> Дата начала</p>
    <input v-model="startDate" type="date" placeholder="Дата начала" />
    <p> Дата конца</p>
    <input v-model="endDate" type="date" placeholder="Дата окончания" />
    <textarea v-model="projectDescription" placeholder="Введите описание проекта"></textarea>
    <button @click="submitProject">Отправить</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
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
    formatToDateTime(date) {
      return `${date}T00:00:00`; // Преобразует в формат `YYYY-MM-DDT00:00:00`
    },
    async submitProject() {
      // Проверка, чтобы все поля были заполнены
      if (!this.projectName || !this.startDate || !this.endDate || !this.projectDescription) {
        this.errorMessage = 'Пожалуйста, заполните все поля';
        return;
      }

      const dataToSend = {
        name: this.projectName,
        description: this.projectDescription,
        start_date: this.formatToDateTime(this.startDate),
        end_date: this.formatToDateTime(this.endDate),
      };

      try {
        const res = await axios.post('/api/projects/create', dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        alert('Проект успешно создан!');
        this.$router.push('/main');
        console.log(res);
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }
      // Логика отправки проекта
      // console.log('Название проекта:', this.projectName);
      // console.log('Дата начала:', this.startDate);
      // console.log('Дата окончания:', this.endDate);
      // console.log('Описание проекта:', this.projectDescription);

      // Здесь можно добавить логику для отправки данных на сервер
      //this.errorMessage = ''; // Очистка ошибки, если все поля заполнены
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
