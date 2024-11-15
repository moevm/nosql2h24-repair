<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="task-page">
    <div class="task-header">
      <div>
        <h1>Ремонт кафедры МОЭВМ</h1>
        <p>СПбГЭТУ "ЛЭТИ"</p>
        <div class="task-title">
          <input
              v-model="taskName"
              :class="{'input-error': !taskName && showErrors}"
              type="text"
              placeholder="Название нового этапа"
              class="stage-name-input"
          />
        </div>
      </div>
    </div>

    <div class="task-content">
      <div class="task-description">
        <textarea v-model="taskDescription" rows="20"></textarea>
      </div>

      <div class="task-dates-status">
        <div class="task-dates">
          <div class="task-date">
            <p>Начало</p>
            <input type="date" v-model="startDate" />
          </div>
          <div class="task-date">
            <p>Конец</p>
            <input type="date" v-model="endDate"  />
          </div>
        </div>
        <div class="task-status">
          <p>Статус</p>
          <select v-model="status">
            <option value="В процессе">В процессе</option>
            <option value="Нет статуса">Нет статуса</option>
            <option value="Опоздание">Опоздание</option>
            <option value="Готово">Готово</option>
          </select>
        </div>
      </div>

      <div class="task-contacts">
        <ContactsComponent />
      </div>
    </div>
    <div class="task-title">
      <button @click="toggleAdd">Сохранить</button>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import ContactsComponent from '../project/ContactsComponent.vue';
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { getProjectId, getStageId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ContactsComponent
  },
  data() {
    return {
      taskName: '',
      startDate: '',
      endDate: '',
      status: '',
      taskDescription: '',
      errorMessage: '',
      showErrors: false
    };
  },
  methods: {
    async toggleAdd() {
      this.showErrors = true;
      if (this.taskName && this.taskDescription && this.startDate && this.endDate && this.status) {
        const dataToSend = {
          name: this.taskName,
          description: this.taskDescription,
          status: this.status,
          start_date: this.formatToDateTime(this.startDate),
          end_date: this.formatToDateTime(this.endDate),
        };
        try {
          const res = await axios.post(`/api/tasks/create/${getProjectId()}/${getStageId()}`, dataToSend, {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
          console.log(res);
          this.showErrors = false;
          alert('Этап задача успешно создана!');
          this.$router.push(`/tasks`);
        } catch (error) {
          console.error("Ошибка сети:", error.message);
          if (error.response && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          }
        }
      } else {
        this.errorMessage = 'Пожалуйста, заполните все поля.';
      }
    },
    formatToDateTime(date) {
      return `${date}T00:00:00`;
    },
  }
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

.task-title button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-title button:hover {
  background-color: #0056b3;
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

.task-description p {
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

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
