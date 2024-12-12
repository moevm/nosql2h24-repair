<template>
    <div class="task-page">
      <h2>Задачи</h2>
      <div class="filter-container">
        <div class="date-filter">
          <input
              type="date"
              v-model="startDate"
              class="large-input"
              :max="endDate"
          />
          <span>-</span>
          <input
              type="date"
              v-model="endDate"
              class="large-input"
              :min="startDate"
          />
        </div>
        <div class="project-filter">
          <input
            type="text"
            v-model="projectName"
            placeholder="Название проекта"
            class="search-input"
          />
          <input
            type="text"
            v-model="taskName"
            placeholder="Название задачи"
            class="search-input"
          />
        </div>
        <div class="status-filter">
          <label for="status">Статус</label>
          <select v-model="selectedStatus">
            <option v-for="status in statuses" :key="status.text" :value="status.text === 'Все'? '': status.text ">
              {{ status.text }}
            </option>
          </select>
        </div>
        <button @click="applyFilters">Применить</button>
        <button @click="resetFilters">Сбросить</button>
      </div>
  
      <div class="task-list">
        <TaskCard
            v-for="task in tasks"
            :key="task.taskId"
            :description="task.description"
            :endDate="task.endDate"
            :startDate="task.startDate"
            :name="task.name"
            :status="task.status"
            :projectName="task.projectName"
            :id="task.taskId"
            :projectId="task.projectId"
            :stageId="task.stageId"
        />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import TaskCard from './TaskCard.vue';
  import {clearAllCookies} from "@/src/js/useCookies";
  
  export default {
    components: {
      TaskCard
    },
    data() {
      return {
        startDate: '',
        endDate: '',
        projectName: '',
        taskName: '',
        selectedStatus: '',
        projects: ['Ремонт кафедры МОЗВМ'], // Пример списка проектов
        statuses: [
          { text: 'Готово', color: 'green' },
          { text: 'Опоздание', color: 'red' },
          { text: 'В процессе', color: 'orange' },
          { text: 'Все', color: '#e0e0e0' },
          { text: 'Нет статуса', color: '#e0e0e0' }
        ],
        tasks: [
          // { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'Готово' },
          // { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'В процессе' },
          // { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: 'Опоздание' },
          // { name: 'Прибить полки', startDate: '2024-12-25', endDate: '2024-12-25', project: 'Ремонт кафедры МОЗВМ', status: '-не выбрано-' },
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
      formatToDateTime(date) {
        return `${date}T00:00:00`;
      },
      async applyFilters() {
        try {
          const params = new URLSearchParams({
          });

          if (this.endDate) {
            params.append('end_date', this.formatToDateTime(this.endDate));
          }
          if(this.startDate) {
            params.append('start_date', this.formatToDateTime(this.startDate));
          }
          if (this.projectName) {
            params.append('project_name', this.projectName);
          }
          if(this.taskName) {
            params.append('task_name', this.taskName);
          }
          if(this.selectedStatus) {
            params.append('task_status', this.selectedStatus);
          }
          const response = await axios.get(`/api/tasks/get_all/?${params.toString()}`);
          this.tasks = Object.values(response.data).map(task => ({
            name: task.name,
            startDate: this.formatDate(task.start_date),
            endDate: this.formatDate(task.end_date),
            status: task.status,
            description: task.description,
            taskId: task.id,
            stageId: task.stage_id,
            projectId:task.project_id,
            projectName: task.project_name,
          }));
          // console.log(response.data);
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');
            clearAllCookies();
            this.$router.push("/login");
          }
          console.error('Ошибка при загрузке контактов:', error);
          if (error.response && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          }
        }
      },
      async fetchTasks() {
        try {
          const response = await axios.get('/api/tasks/get_all');
          console.log(response.data);
          this.tasks = Object.values(response.data).map(task => ({
            name: task.name,
            startDate: this.formatDate(task.start_date),
            endDate: this.formatDate(task.end_date),
            status: task.status,
            description: task.description,
            taskId: task.id,
            stageId: task.stage_id,
            projectId:task.project_id,
            projectName: task.project_name,
          }));
          // console.log(this.tasks)
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          console.error('Ошибка при загрузке проектов:', error);
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
        const year = date.getFullYear();
        return `${day}.${month}.${year}`;
      },
      resetFilters() {
          this.startDate = '';
          this.endDate = '';
          this.projectName = '';
          this.taskName = '';
          this.selectedStatus = '';
          this.fetchTasks();
        }
    },
    beforeMount() {
      this.fetchTasks();
    },
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
