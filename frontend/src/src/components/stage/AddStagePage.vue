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
              :class="{'input-error': !newStageName && showErrors}"
              type="text"
              placeholder="Название нового этапа"
              class="stage-name-input"
          />
          <input
              v-model="newStageStartDate"
              :class="{'input-error': !newStageStartDate && showErrors}"
              type="date"
              class="stage-date-input"
          />
          <input
              v-model="newStageEndDate"
              :class="{'input-error': !newStageEndDate && showErrors}"
              type="date"
              class="stage-date-input"
          />
          <button @click="addStage">Добавить этап</button>

          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { getProjectId } = useCookies();

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
      errorMessage: '',
      showErrors: false,
    };
  },
  methods: {
    async addStage() {
      this.showErrors = true;

      if (this.newStageName && this.newStageStartDate && this.newStageEndDate) {
        const dataToSend = {
          name: this.newStageName,
          start_date: this.formatToDateTime(this.newStageStartDate),
          end_date: this.formatToDateTime(this.newStageEndDate),
        };
        try {
          const res = await axios.post(`/api/projects/${getProjectId()}/add_stage`, dataToSend, {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
          console.log(res);
          alert('Этап успешно создан!');
          this.$router.push(`/stages`);
        } catch (error) {
          console.error("Ошибка сети:", error.message);
          if (error.response && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          }
        }
      } else {
        this.errorMessage='Пожалуйста, заполните все поля.';
      }
    },
    formatToDateTime(date) {
      return `${date}T00:00:00`;
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
  background-color: #625b71;
  color: white;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.add-stage-form button:hover {
  background-color: #554a6d;
}
.input-error {
  border-color: red;
}
.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
