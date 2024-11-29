<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="risk-details">
    <h1>Детали риска</h1>
    <div v-if="riskName">
      <div v-if="isEditing">
        <input v-model="riskName" class="edit-title" />
        <textarea v-model="riskDescription" class="edit-description"></textarea>
        <div class="button-group">
          <button @click="saveRisk" class="button">Сохранить</button>
          <button @click="cancelEdit" class="cancel-button">Отмена</button>
        </div>
      </div>
      <div v-else>
        <h2>{{ riskName }}</h2>
        <p>{{ riskDescription }}</p>
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
import { useCookies } from '@/src/js/useCookies';
const { getProjectId,getRiskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
  },
  data() {
    return {
      riskName:"",
      riskDescription:"",
      risk: null,
      editedRisk: null,
      isEditing: false,
      // tasks: [
      //   // { id: 1, title: 'Износ, поломка', description: 'Студенты могут разбить дорогой кафель...' },
      //   // { id: 2, title: 'Задержка в работах', description: 'Из-за санкций некоторые материалы...' },
      //   // Добавьте дополнительные риски сюда
      // ],
    };
  },
  // created() {
  //   const taskId = parseInt(this.$route.params.taskId);
  //   this.risk = this.tasks.find(task => task.id === taskId);
  // },
  methods: {
    goBack() {
      this.$router.push('/risks');
    },
    editRisk() {
      this.isEditing = true;
      this.editedRisk = { ...this.risk };
    },
    saveRisk() {
      this.risk.title = this.editedRisk.title;
      this.risk.description = this.editedRisk.description;
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
        this.riskName = response.data.risk.name;
        this.riskDescription = response.data.risk.description;
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
}

.cancel-button {
  padding: 8px 16px;
  background-color: #625b71;
  color: white;
  border: none;
  cursor: pointer;
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
