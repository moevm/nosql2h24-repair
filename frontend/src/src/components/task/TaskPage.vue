<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="task-page">
    <div class="task-header">
      <div>
        <h1>{{projectName}}</h1>
        <div class="task-title">
          <h2>Этап: {{stageName}}</h2>
          <h2>Задача: </h2>
          <h2 v-if="!isEditing">{{taskName}}</h2>
          <input v-else type="text" v-model="taskName" class="task-name-input" />
          <button v-if="!isEditing" @click="startEdit">Редактировать</button>
          <button v-if="isEditing" @click="saveEdit">Сохранить</button>
          <button v-if="isEditing" @click="cancelEdit">Отмена</button>
        </div>
      </div>
    </div>

    <div class="task-content">
      <div class="task-description">
        <textarea v-if="isEditing" v-model="taskDescription" rows="5"></textarea>
        <p v-else>{{ taskDescription }}</p>
      </div>

      <div class="task-dates-status">
        <div class="task-dates">
          <div class="task-date">
            <p>Начало</p>
            <input type="date" v-model="startDate" :disabled="!isEditing" />
          </div>
          <div class="task-date">
            <p>Конец</p>
            <input type="date" v-model="endDate" :disabled="!isEditing" />
          </div>
        </div>
        <div class="task-status">
          <p>Статус</p>
          <select v-model="status" :disabled="!isEditing">
            <option value="В процессе">В процессе</option>
            <option value="Нет статуса">Нет статуса</option>
            <option value="Опоздание">Опоздание</option>
            <option value="Готово">Готово</option>
          </select>
        </div>
      </div>

      <div class="task-contacts">
        <ContactsComponent :contacts="contacts" :isEditing="isEditing" @delete="deleteWorker" />
      </div>
    </div>

    <div class="task-actions">
      <button @click="goToTasks" class="go-to-tasks-button">Перейти к задачам</button>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import ContactsComponent from '../project/ContactsComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId,getProjectName,getStageId,getStageName,getTaskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ContactsComponent
  },
  data() {
    return {
      contacts: [],
      projectName: getProjectName(),
      stageName: getStageName(),
      taskName: "",
      isEditing: false,
      startDate: "",
      endDate: "",
      status: "",
      taskDescription: ``,
      originalTaskName: "",
      originalStartDate: "",
      originalEndDate: "",
      originalStatus: "",
      originalTaskDescription: "",
    };
  },
  methods: {
    deleteWorker(id){
      this.contacts = this.contacts.filter(contact => contact.id !== id);
    },
    async fetchTaskData() {
      try {
        const response = await axios.get(`/api/tasks/get_task/${getProjectId()}/${getStageId()}/${getTaskId()}`);
        console.log(response.data);
        this.taskName = response.data.name;
        this.startDate = this.formatDate(response.data.start_date);
        this.endDate = this.formatDate(response.data.end_date);
        this.status= response.data.status;
        this.taskDescription = response.data.description;
        this.taskId= response.data.id;
        this.contacts = Object.entries(response.data.workers).map(([id, contact]) => ({
          id, // ID пользователя (ключ объекта)
          userName: contact.name,
          role: contact.role,
        }));
        console.log(this.contacts);
      } catch (error) {
        console.error('Ошибка при загрузке Задачи:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
    formatToDateTime(date) {
      return `${date}T00:00:00`; // Преобразует в формат `YYYY-MM-DDT00:00:00`
    },
    startEdit() {
      this.originalTaskName = this.taskName;
      this.originalStartDate = this.startDate;
      this.originalEndDate = this.endDate;
      this.originalStatus = this.status;
      this.originalTaskDescription = this.taskDescription;
      this.isEditing = true;
    },
    async saveEdit() {
      const dataToSend = {
        name: this.taskName,
        description: this.taskDescription,
        status: this.status,
        start_date: this.formatToDateTime(this.startDate),
        end_date: this.formatToDateTime(this.endDate),
      };
      console.log(dataToSend)
      try {
        await axios.put(`/api/tasks/update_task/${getProjectId()}/${getStageId()}/${getTaskId()}`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        this.$emit('update-stage', { ...this.stage, ...this.editStageData });
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }

      console.log("Сохранено:", this.startDate, this.endDate, this.status, this.taskDescription);
      this.isEditing = false;
    },
    cancelEdit() {
      this.taskName = this.originalTaskName;
      this.startDate = this.originalStartDate;
      this.endDate = this.originalEndDate;
      this.status = this.originalStatus;
      this.taskDescription = this.originalTaskDescription;
      this.isEditing = false;
    },
    goToTasks() {
      this.$router.push(`/tasks`);
    }
  },
  beforeMount() {
    this.fetchTaskData();
  },
};
</script>

<style scoped>
.task-page {
  padding: 20px;
  margin-left: 150px;
  margin-top: 60px;
}

.task-header h1 {
  font-size: 24px;
}

.task-header p {
  font-size: 18px;
  color: #666;
}

.task-title {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.task-title h2 {
  font-size: 20px;
  margin-right: 10px;
}

.task-title input.task-name-input {
  font-size: 20px;
  margin-right: 10px;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.task-title button {
  padding: 8px 12px;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  margin-right: 15px;
}

.task-title button:hover {
  background-color: #4f416d;
}

.task-content {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.task-description {
  flex: 1;
  width: 80%;
}

.task-description p{
  width: 80%;
}

.task-description textarea {
  width: 80%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.task-dates-status {
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 14px;
}

.task-dates {
  display: flex;
  gap: 20px;
}

.task-date input[type="date"] {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.task-status select {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.task-contacts {
  margin-left: 20px;
}

.task-actions {
  margin-top: 20px;
}

.go-to-tasks-button {
  padding: 8px 12px;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
}

.go-to-tasks-button:hover {
  background-color: #4f416d;
}
</style>
