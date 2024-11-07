<template>
  <div class="stages-page">
    <HeaderComponent />
    <ProjectSidebarComponent />
    <div class="main-content">
      <div class="stages-container">
        <div class="header-container">
          <div class="header">
            <h2>Ремонт кафедры МОЭВМ</h2>
            <p>СПбГЭТУ "ЛЭТИ"</p>
          </div>
          <input type="text" v-model="search" placeholder="Название этапа" />
        </div>

        <StageComponent
          v-for="stage in filteredStages"
          :key="stage.id"
          :stage="stage"
          @edit="editStage"
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
        { id: 1, name: "Покрасить", startDate: "25.12.2024", endDate: "26.12.2024" },
        { id: 2, name: "Вырастить", startDate: "02.12.2024", endDate: "25.12.2024" },
        { id: 3, name: "Родить", startDate: "25.12.2024", endDate: "25.12.2024" },
      ],
    };
  },
  computed: {
    filteredStages() {
      return this.stages.filter(stage => stage.name.includes(this.search));
    },
  },
  methods: {
    searchStages() {
      alert(`Поиск этапов по запросу: "${this.search}"`);
    },
    editStage(stage) {
      alert(`Редактирование этапа: ${stage.name}`);
      // Реализуйте логику для открытия формы редактирования этапа
    },
    deleteStage(stageId) {
      this.stages = this.stages.filter(stage => stage.id !== stageId);
      alert(`Этап с ID ${stageId} удален`);
    },
    goToTasks(stageId) {
      alert(`Переход к задачам этапа с ID ${stageId}`);
      // Реализуйте логику для перехода к списку задач
    },
  },
};
</script>

<style scoped>
.stages-page {
  display: flex;
  flex-direction: column;
}
.main-content {
  display: flex;
  margin-left: 150px;
  padding-top: 60px;
}
.stages-container {
  flex: 1;
  padding: 16px;
}
.header-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.header {
  margin-right: 16px;
}
.stages-container input {
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-left: 8%;
}
.stages-container button {
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>