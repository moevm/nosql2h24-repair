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
            :taskName="task.taskName"
            :class="{ selected: selectedTaskId === task.taskId}"
            @click="selectTask(task)"
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
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId, getStageId, getStageName,setTaskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
  },
  data() {
    return {
      taskName: '',
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
    async deleteTask(taskId) {
      if (confirm(`Удалить задачу ${this.taskName}?`)) {
        try {
          await axios.delete(`/api/tasks/delete/${getProjectId()}/${getStageId()}/${taskId}`, {
            headers: {
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
          this.tasks = this.tasks.filter(task => task.taskId !== taskId);
          this.selectedTaskId = null;  // сбрасываем выбор после удаления
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          // Обработка ошибки, если нужно
          console.error(error);
        }
      }

    },
    viewTask() {
      setTaskId(this.selectedTaskId);
      this.$router.push(`/tasks/viewRedactorTask`);
    },
    selectTask(task) {
      this.selectedTaskId = task.taskId;
      this.taskName = task.taskName;
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

button {
  padding: 5px 10px;
  margin-right: 10px;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  border-radius: 10px;
}

button:hover {
  background-color: #4d4069;
}
</style>
