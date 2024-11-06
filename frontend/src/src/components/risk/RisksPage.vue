<template>
  <div class="main-container">
    <HeaderComponent />
    <ProjectSidebarComponent />

    <div class="content">
      <div class="task-container">
        <div class="search-bar">
          <div>
            <h1>Ремонт кафедры МОЭВМ</h1>
            <p>СПбГЭТУ "ЛЭТИ"</p>
          </div>
          <input type="text" placeholder="Название риска" v-model="searchQuery" class="search-input" />
        </div>

        <!-- Кнопка добавления -->
        <button class="add-button" @click="goToAddTask">+ Добавить</button>
        
        <!-- Список задач -->
        <TaskItemComponent
          v-for="task in filteredTasks"
          :key="task.id"
          :title="task.title"
          :description="task.description"
          @delete="deleteTask(task.id)"
          @details="viewDetails(task.id)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import TaskItemComponent from '../risk/TaskItemComponent.vue';

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    TaskItemComponent,
  },
  data() {
    return {
      searchQuery: '',
      tasks: [
        { id: 1, title: 'Износ, поломка', description: 'Студенты могут разбить дорогой кафель. ...' },
        { id: 2, title: 'Задержка в работах', description: 'Из-за санкций некоторые материалы ...' },
      ],
    };
  },
  computed: {
    filteredTasks() {
      return this.tasks.filter(task => 
        task.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    goToAddTask() {
      this.$router.push({ path: '/add-risk', query: { editing: false } });
    },
    addTask(newTask) {
      this.tasks.push(newTask);
    },
    deleteTask(id) {
      this.tasks = this.tasks.filter(task => task.id !== id);
    },
    viewDetails(taskId) {
      this.$router.push({ path: `/risk-details/${taskId}` });
    },
  },
};
</script>

<style scoped>
/* Основные стили */
.main-container {
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
}

.content {
  display: flex;
  margin-left: 150px;
  padding-top: 60px;
}

/* Стили для верхнего компонента */
header-component {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #f8f8f8;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Стили для бокового меню */
sidebar-component {
  width: 200px;
  background-color: #e8e8e8;
  padding: 15px;
}

/* Стили для основного содержимого */
.task-container {
  flex: 1;
  padding: 20px;
}

.search-bar {
  top: 60px; /* Высота верхнего бара */
  left: 200px; /* Ширина бокового бара */
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 10px 20px;
}

.add-button {
  margin-top: 10px;
  padding: 5px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.task-item {
  background-color: #f1f1f1;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}

.search-input {
  width: 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>