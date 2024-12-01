<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="risk-details">
    <h1>Детали риска</h1>
    <div v-if="risk.name">
      <div v-if="isEditing">
        <input v-model="risk.name" class="edit-title" />
        <textarea v-model="risk.description" class="edit-description"></textarea>
        <div class="button-group">
          <button @click="saveRisk" class="button">Сохранить</button>
          <button @click="cancelEdit" class="cancel-button">Отмена</button>
        </div>
      </div>
      <div v-else>
        <h2>{{ risk.name }}</h2>
        <p>{{ risk.description }}</p>
        <div class="button-group">
          <button @click="editRisk" class="button">Редактировать</button>
          <button @click="goBack" class="button">Назад</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Риск не найден.</p>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId,getRiskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
  },
  data() {
    return {
      editedRisk: null,
      isEditing: false,
      risk: [
      ],
    };
  },
  methods: {
    goBack() {
      this.$router.push('/risks');
    },
    editRisk() {
      this.isEditing = true;
      this.editedRisk = { ...this.risk };
    },
    async saveRisk() {
      const dataToSend = {
        name: this.risk.name,
        description: this.risk.description,
      };
      console.log(dataToSend)
      try {
        const res = await axios.put(`/api/projects/${getProjectId()}/update_risk/${getRiskId()}`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
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
      this.isEditing = false;
    },
    cancelEdit() {
      this.isEditing = false;
      this.editedRisk = null;
    },
    async fetchRiskData() {
      try {
        const response = await axios.get(`/api/projects/${getProjectId()}/get_risk/${getRiskId()}`);
        console.log(response.data);
        this.risk = {
          id: response.data.risk.id, // Можно сохранить ID для идентификации риска
          name: response.data.risk.name,
          description: response.data.risk.description,
        };

        // Добавляем риск в массив
        console.log(this.risk);
        // console.log(this.riskName);
      } catch (error) {
        console.error('Ошибка при загрузке Риска:', error);
      }
    },
  },
  beforeMount() {
    this.fetchRiskData();
  },
};
</script>

<style scoped>
.risk-details {
  padding: 20px;
  margin-left: 150px;
  margin-top: 60px;
}

.button-group {
  display: flex;
  gap: 10px; /* Увеличение расстояния между кнопками */
  margin-top: 10px;
}

.button {
  padding: 8px 16px;
  background-color: #625b71;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 10px;
}

.cancel-button {
  padding: 8px 16px;
  background-color: #625b71;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 10px;
}

.edit-title {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

.edit-description {
  width: 100%;
  height: 100px;
  padding: 8px;
  margin-bottom: 10px;
  resize: vertical;
}
</style>
