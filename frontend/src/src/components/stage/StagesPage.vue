<template>
  <div class="stages-page">
    <HeaderComponent />
    <ProjectSidebarComponent />
    <div class="main-content">
      <div class="stages-container">
        <div class="header-container">
          <!-- Контейнер для заголовка -->
          <div class="header-left">
            <h2>Ремонт кафедры МОЭВМ</h2>
            <p>СПбГЭТУ "ЛЭТИ"</p>
          </div>

          <!-- Контейнер для поля поиска и кнопки -->
          <div class="header-right">
            <input type="text" v-model="search" placeholder="Название этапа" />
            <button @click="goToAddStagePage" class="add-stage-button">
              Добавить этап
            </button>
          </div>
        </div>

        <StageComponent
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
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import StageComponent from './StageComponent.vue';

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    StageComponent,
  },
  data() {
    return {
      search: '',
      stages: [
        { id: 1, name: "Покрасить", startDate: "2024-12-25", endDate: "2024-12-26" },
        { id: 2, name: "Вырастить", startDate: "2024-12-02", endDate: "2024-12-25" },
        { id: 3, name: "Родить", startDate: "2024-12-25", endDate: "2024-12-25" },
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
      const index = this.stages.findIndex(stage => stage.id === updatedStage.id);
      if (index !== -1) {
        this.stages.splice(index, 1, updatedStage);
      }
    },
    deleteStage(stageId) {
      this.stages = this.stages.filter(stage => stage.id !== stageId);
    },
    goToTasks(stageId) {
      this.$router.push(`/tasks-list/${stageId}`);
    },
    goToAddStagePage() {
      this.$router.push({ name: 'add-stage' });
    },
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
  padding-top: 60px;
  width: calc(100% - 150px);
}

.stages-container {
  flex: 1;
  padding: 16px;
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
  background-color: #4CAF50;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px; /* Добавляем отступ для кнопки */
}

.add-stage-button:hover {
  background-color: #45a049;
}
</style>