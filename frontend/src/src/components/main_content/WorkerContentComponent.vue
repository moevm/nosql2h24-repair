<template>
    <div class="task-page">
      <h2>Задачи</h2>
      <div class="filter-container">
        <div class="date-filter">
          <input type="date" v-model="startDate" class="large-input" />
          <span>-</span>
          <input type="date" v-model="endDate" class="large-input" />
        </div>
        <div class="project-filter">
          <label for="project">Проект</label>
          <select v-model="selectedProject">
            <option value="">Value</option>
            <option v-for="project in projects" :key="project" :value="project">
              {{ project }}
            </option>
          </select>
        </div>
        <div class="status-filter">
          <label for="status">Статус</label>
          <select v-model="selectedStatus">
            <option value="">Value</option>
            <option v-for="status in statuses" :key="status.text" :value="status.text">
              {{ status.text }}
            </option>
          </select>
        </div>
        <button @click="applyFilters">Применить</button>
      </div>
  
      <div class="task-list">
        <TaskCard
          v-for="(task, index) in filteredTasks"
          :key="index"
          :task="task"
        />
      </div>
    </div>
  </template>
  
  <script>
  import TaskCard from './TaskCard.vue';
  
  export default {
    components: {
      TaskCard
    },
    data() {
      return {
        startDate: '',
        endDate: '',
        selectedProject: '',
        selectedStatus: '',
        projects: ['Ремонт кафедры МОЗВМ'], // Пример списка проектов
        statuses: [
          { text: 'Готово', color: 'green' },
          { text: 'Опоздание', color: 'red' },
          { text: 'В процессе', color: 'orange' },
          { text: '-не выбрано-', color: '#e0e0e0' }
        ],
        tasks: [
          { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'Готово' },
          { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'В процессе' },
          { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'Опоздание' },
          { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: '-не выбрано-' },
        ]
      };
    },
    computed: {
      filteredTasks() {
        return this.tasks.filter(task => {
          const matchesDateRange =
            (!this.startDate || task.startDate >= this.startDate) &&
            (!this.endDate || task.endDate <= this.endDate);
  
          const matchesProject = !this.selectedProject || task.project === this.selectedProject;
          const matchesStatus = !this.selectedStatus || task.status === this.selectedStatus;
  
          return matchesDateRange && matchesProject && matchesStatus;
        });
      }
    },
    methods: {
      applyFilters() {
        // Здесь можно будет применить дополнительные фильтры, если нужно
      }
    }
  };
  </script>
  
  <style scoped>
.task-page {
  padding: 20px;
  margin-top: 60px;
  margin-left: 150px;
}

h2 {
  text-align: left;
  color: #6e6b93;
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  margin-bottom: 20px;
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
  margin-left: 10px;
}

button:hover {
  background-color: #5c5583;
}

.task-list {
  display: flex;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}
  </style>  