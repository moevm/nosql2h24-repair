<template>
  <div class="stages-page">
    <HeaderComponent />
    <SidebarComponent />
    <div class="main-content">
      <div class="stages-container">
        <div class="header-container">
          <!-- Контейнер для заголовка -->
          <div class="header-left">
            <h1>{{projectName}}</h1>
<!--            <p>СПбГЭТУ "ЛЭТИ"</p>-->
          </div>

          <!-- Контейнер для поля поиска и кнопки -->
          <div class="header-right">
            <input type="text" v-model="search" placeholder="Название этапа" />
            <button @click="goToAddStagePage" class="add-stage-button">
              Добавить этап
            </button>
          </div>
        </div>

        <StageComponent :projectId="projectId" :projectName="projectName"
          v-for="stage in filteredStages"
          :key="stage.id"
          :stage="stage"
          @update-stage="updateStage"
          @delete="deleteStage"
          @goToTasks="goToTasks"
        />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import StageComponent from './StageComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId, getProjectName } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    StageComponent,
  },

  data() {
    return {
      projectName: getProjectName(),
      search: '',
      stages: [
      ],
    };
  },
  computed: {
    filteredStages() {
      return this.stages.filter(stage => stage.name.includes(this.search));
    },
  },
  methods: {
    updateStage(updatedStage) {
      const index = this.stages.findIndex(stage => stage.stageId === updatedStage.stageId);
      if (index !== -1) {
        this.stages.splice(index, 1, updatedStage);
      }
    },
    deleteStage(stageId) {
      this.stages = this.stages.filter(stage => stage.stageId !== stageId);
    },
    goToTasks() {
      // this.$router.push(`/tasks-list/${stageId}`);
    },
    goToAddStagePage() {
      this.$router.push(`/add-stage`);
      // this.$router.push({ name: 'add-stage' });
    },
    async fetchStageData() {
      try {
        const response = await axios.get(`/api/projects/${getProjectId()}/get_stages`);
        this.stages = Object.values(response.data.stages).map(stage => ({
          name: stage.name,
          startDate: this.formatDate(stage.start_date),
          endDate: this.formatDate(stage.end_date),
          stageId: stage.id,
        }));
        // console.log(this.stages);
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке Этапов:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    },
  },
  beforeMount() {
    this.fetchStageData();
  },
};
</script>

<style scoped>
.stages-page {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.main-content {
  display: flex;
  margin-left: 150px;
  padding-top: 30px;
  width: calc(100% - 150px);
}

.stages-container {
  flex: 1;
  padding: 20px;
}

.header-container {
  display: flex;
  justify-content: space-between; /* Располагаем элементы на разных сторонах */
  align-items: center; /* Центрируем элементы по вертикали */
  margin-bottom: 16px;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-right {
  display: flex;
  align-items: center;
}

.stages-container input {
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-left: 8%;
}

.add-stage-button {
  background-color: #625b71;
  color: white;
  padding: 8px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-left: 10px; /* Добавляем отступ для кнопки */
}

.add-stage-button:hover {
  background-color: #4e4168;
}
</style>
