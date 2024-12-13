<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="task-page">
    <div class="task-header">
      <div>
        <h1>{{ projectName }}</h1>
        <p>{{ stageName }}</p>
        <div class="task-title">
          <input
            v-model="taskName"
            :class="{ 'input-error': !taskName && showErrors }"
            type="text"
            placeholder="Название новой задачи"
            class="stage-name-input"
          />
          <button @click="toggleAdd" class="save-button">Сохранить</button>
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
            <input
                type="date"
                :max="endDate ? endDate : $store.getters.getEndDateStage"
                :min="$store.getters.getStartDateStage"
                v-model="startDate"
            />
          </div>
          <div class="task-date">
            <p>Конец</p>
            <input
                type="date"
                :min="startDate ? startDate : $store.getters.getStartDateStage"
                :max="$store.getters.getEndDateStage"
                v-model="endDate"
            />
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
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import axios from 'axios';
import { clearAllCookies, useCookies } from '@/src/js/useCookies';
const { getProjectId, getStageId, getStageName, getProjectName } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
  },
  data() {
    return {
      projectName: getProjectName(),
      stageName: getStageName(),
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
          if (error.response.status === 401) {
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
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
  margin-bottom: 10px;
}

.task-header p {
  font-size: 18px;
  color: #666;
  margin-bottom: 20px;
}

.task-title {
  align-items: center;
  gap: 10px;
}

.task-title input{
  width: 40%;
  margin-right: 15px;
}

.stage-name-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.input-error {
  border-color: red;
}

.save-button {
  padding: 10px 20px;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-size: 16px;
}

.save-button:hover {
  background-color: #51446e;
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

.task-description textarea {
  width: 90%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
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

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>
