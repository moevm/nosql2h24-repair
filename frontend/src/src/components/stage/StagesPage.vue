<template>
  <div class="stages-page">
    <HeaderComponent />
    <SidebarComponent />
    <div class="main-content">
      <div class="stages-container">
        <div class="header-container">
          <!-- Контейнер для заголовка и фильтров -->
          <div class="header-left">
            <h1>{{ projectName }}</h1>
            <!--            <p>СПбГЭТУ "ЛЭТИ"</p>-->
          </div>
          <div class="filter-container">
            <div class="date-filter">
              <input type="date" v-model="startDate" class="large-input" />
              <span>-</span>
              <input type="date" v-model="endDate" class="large-input" />
            </div>
            <input type="text" v-model="search" placeholder="Название этапа" />
            <button @click="applyFilters">Применить</button>
            <button @click="goToAddStagePage" class="add-stage-button">
              Добавить этап
            </button>
          </div>
        </div>

        <StageComponent
          :projectId="projectId"
          :projectName="projectName"
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
import { clearAllCookies, useCookies } from '@/src/js/useCookies';
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
      startDate: '',
      endDate: '',
      stages: [],
    };
  },
  computed: {
    filteredStages() {
      return this.stages.filter(stage =>
        stage.name.includes(this.search) &&
        (!this.startDate || new Date(stage.startDate) >= new Date(this.startDate)) &&
        (!this.endDate || new Date(stage.endDate) <= new Date(this.endDate))
      );
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
        if (error.response.status === 401) {
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
    applyFilters() {
      // Здесь можно добавить дополнительную логику для применения фильтров
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
  align-items: center; /* Выравниваем элементы по вертикали */
  margin-bottom: 16px;
}

.header-left {
  margin-right: 20px; /* Добавляем отступ между заголовком и фильтрами */
}

.filter-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.date-filter,
.project-filter,
.status-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-filter input {
  margin-left: 5px;
}

.project-filter label,
.status-filter label {
  margin-right: 10px;
}

.large-input {
  padding: 10px;
  margin-left: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

input,
select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #6e6b93;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #5c5583;
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
