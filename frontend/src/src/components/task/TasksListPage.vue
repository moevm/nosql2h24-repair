<template>
  <HeaderComponent/>
  <SidebarComponent/>
  <div class="tasks-list-page">
    <div class="search-header">
      <h2>Задачи этапа: {{ stageName }}</h2>
      <div class="filter-container">
        <div class="date-filter">
          <input type="date" v-model="startDate" class="large-input"/>
          <span>-</span>
          <input type="date" v-model="endDate" class="large-input"/>
        </div>
        <input
            type="text"
            v-model="taskName"
            placeholder="Название задачи"
            class="search-input"
        />
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
    </div>
    <button @click="addTask">Добавить задачу</button>

    <div v-if="paginatedTasks.length">
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
            v-for="task in paginatedTasks"
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

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Предыдущая</button>
      <span>Страница {{ currentPage }} из {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Следующая</button>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';

const {getProjectId, getStageId, getStageName, setTaskId} = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
  },
  data() {
    return {
      taskName: '',
      stageName: getStageName(),
      tasks: [],
      selectedTaskId: null,  // для отслеживания выбранной задачи
      searchQuery: '',  // для поиска задачи по названию
      statuses: [
        {text: 'Готово'},
        {text: 'Опоздание'},
        {text: 'В процессе'},
        {text: 'Все'},
        {text: 'Нет статуса'}
      ],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  computed: {
    filteredTasks() {
      return this.tasks.filter(task =>
          task.taskName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    paginatedTasks() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTasks.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTasks.length / this.itemsPerPage);
    },
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
          if (error.response.status === 401) {
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
        if (error.response.status === 401) {
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке Этапов:', error);
      }
    },
    formatToDateTime(date) {
      return `${date}T00:00:00`;
    },
    async applyFilters() {
      try {
        const params = new URLSearchParams({});

        if (this.endDate) {
          params.append('end_date', this.formatToDateTime(this.endDate));
        }
        if (this.startDate) {
          params.append('start_date', this.formatToDateTime(this.startDate));
        }
        if (this.taskName) {
          params.append('task_name', this.taskName);
        }
        if (this.selectedStatus) {
          params.append('task_status', this.selectedStatus);
        }
        const response = await axios.get(`/api/tasks/get_stage_tasks/${getProjectId()}/${getStageId()}/?${params.toString()}`);
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
        this.currentPage = 1; // Сброс текущей страницы после применения фильтров
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
      return `${day}.${month}.${year}`;
    },
    resetFilters() {
      this.startDate = '';
      this.endDate = '';
      this.taskName = '';
      this.selectedStatus = '';
      this.fetchTaskData();
      this.currentPage = 1; // Сброс текущей страницы после сброса фильтров
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
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

.search-input {
  width: 300px;
  padding-left: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-header {
  gap: 20px;
  display: flex;
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

.filter-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
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
  margin-left: 10px;
}

button:hover {
  background-color: #5c5583;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #6e6b93;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 10px;
}

.pagination button:hover {
  background-color: #5c5583;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>