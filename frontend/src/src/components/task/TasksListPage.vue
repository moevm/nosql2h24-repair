<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="tasks-list-page">
    <h2>Задачи этапа: {{ stageName }}</h2>

    <button @click="addTask">Добавить задачу</button>

    <div v-if="tasks.length">
      <table class="task-table">
        <thead>
          <tr>
            <th>Название задачи</th>
            <th>Начало</th>
            <th>Конец</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="task in tasks" 
            :key="task.taskId"
            :class="{ selected: selectedTaskId === task.taskId }"
            @click="selectTask(task.taskId)"
          >
            <td>{{ task.taskName }}</td>
            <td>{{ task.startDate }}</td>
            <td>{{ task.endDate }}</td>
            <td>{{ task.status }}</td>
          </tr>
        </tbody>
      </table>
      
      <div class="task-actions" v-if="selectedTaskId">
        <button @click="viewTask(selectedTaskId)">Описание</button>
        <button @click="deleteTask(selectedTaskId)">Удалить</button>
      </div>
    </div>
    <div v-else>
      <p>Задачи отсутствуют для этого этапа.</p>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { getProjectId, getStageId, getStageName,setTaskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
  },
  data() {
    return {
      stageName: getStageName(),
      tasks: [
      ],
      selectedTaskId: null  // для отслеживания выбранной задачи
    };
  },
  methods: {
    addTask() {
      this.$router.push(`/add_task`); // переход на страницу новой задачи
    },
    deleteTask(taskId) {
      this.tasks = this.tasks.filter(task => task.id !== taskId);
      this.selectedTaskId = null;  // сбрасываем выбор после удаления
    },
    viewTask() {
      setTaskId(this.selectedTaskId);
      this.$router.push(`/tasks/viewRedactorTask`);
    },
    selectTask(taskId) {
      this.selectedTaskId = taskId;
    },
    async fetchTaskData() {
      try {
        const response = await axios.get(`/api/tasks/get_stage_tasks/${getProjectId()}/${getStageId()}`);
        // console.log(response.data);
        this.tasks = Object.values(response.data).map(task => ({
          taskName: task.name,
          startDate: this.formatDate(task.start_date),
          endDate: this.formatDate(task.end_date),
          status: task.status,
          taskDescription: task.description,
          taskId: task.id
        }));
        console.log(this.tasks);
      } catch (error) {
        console.error('Ошибка при загрузке Этапов:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    },
  },
  beforeMount() {
    this.fetchTaskData();
  },
};
</script>

<style scoped>
.tasks-list-page {
  padding: 20px;
  margin-left: 150px;
  margin-top: 60px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.task-table th, .task-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.task-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  text-align: left;
}

.task-table td {
  text-align: left;
}

.task-table tr:hover {
  background-color: #f5f5f5;
}

.task-table tr.selected {
  background-color: #e0f7fa; /* Подсветка выбранной задачи */
}

.task-actions {
  margin-top: 20px;
}

.task-actions button {
  padding: 5px 10px;
  margin-right: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-actions button:hover {
  background-color: #0056b3;
}
</style>
