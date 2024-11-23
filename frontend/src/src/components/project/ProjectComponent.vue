<template>
  <div class="project-card">
    <h2 class="project-title">{{ projectName }}</h2>
    <p class="project-location">{{ projectLocation }}</p>
    <p class="project-dates">Начало: {{ startDate }}</p>
    <p class="project-dates">Конец: {{ endDate }}</p>
    <div class="project-status">
      Статус
<!--      <span class="phase">{{ projectPhase }}</span>-->
      <span class="status">{{ projectPhase }}</span>
    </div>
    <button class="project-button" @click="goToProject">Страница проекта</button>
  </div>
</template>

<script>
import { useCookies } from '@/src/js/useCookies';
const { setProjectId, setProjectName } = useCookies();

export default {
  props: {
    projectName: {
      type: String,
      required: true,
    },
    projectLocation: {
      type: String,
      required: true,
    },
    projectId:{
      type: String,
      required: true,
    },
    startDate: {
      type: String,
      required: true,
    },
    endDate: {
      type: String,
      required: true,
    },
    projectPhase: {
      type: String,
      default: 'Основной этап',
    },
    projectStatus: {
      type: String,
      default: 'В процессе',
    },
  },
  methods: {
    goToProject() {
      // Логика перехода на страницу проекта
      setProjectId(this.projectId);
      setProjectName(this.projectName);
      this.$router.push(`/project`);
    },
  },
};
</script>

<style scoped>
.project-card {
  position: relative; /* Устанавливает относительное позиционирование для внутренних элементов */
  width: 500px;
  height: 350px;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 5px; /* Отступы между карточками проекта */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Размещает элементы с равным пространством между ними */
}

.p{
  margin: 0; /* Убираем отступы */
  padding: 0; /* Убираем внутренние отступы */
}

.project-title,
.project-location,
.project-dates,
.project-status {
  margin: 0; /* Убираем отступы */
  padding: 0; /* Убираем внутренние отступы */
}

.project-title {
  font-size: 20px;
  font-weight: bold;
}

.project-location,
.project-dates {
  font-size: 16px;
}

.project-status {
  display: flex;
  justify-content: space-between;
}

.phase,
.status {
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #e0e0e0; /* Фоновый цвет для блока статуса */
}

.project-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.project-button:hover {
  background-color: #0056b3; /* Цвет кнопки при наведении */
}
</style>
