<template>
  <div class="content">
    <div class="header-search">
      <h1>Проекты</h1>
      <div class="filter-container">
        <p>Интервал выполнения</p>
        <div class="date-filter">
          <input
              type="date"
              v-model="startDate"
              class="large-input"
          />
          <span>-</span>
          <input
              type="date"
              v-model="endDate"
              class="large-input"
          />
        </div>
        <input
            type="text"
            v-model="projectName"
            placeholder="Поиск проекта"
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
    <div class="projects-container">
      <div v-for="(item, index) in paginatedItems" :key="index" class="project-item">
        <Project
            v-if="item.type === 'project'"
            :projectName="item.name"
            :project-location="item.projectLocation"
            :startDate="item.startDate"
            :endDate="item.endDate"
            :project-phase="item.projectPhase"
            :projectStatus="item.status"
            :projectId="item.projectId"
        />
        <NewProjectButton v-if="item.type === 'newProjectButton' && userRole !== 'Рабочий' && userRole !== 'Прораб'" />
      </div>
    </div>
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Предыдущая</button>
      <span>
        <template v-if="currentPage > 2">
          <button @click="goToPage(1)">1</button>
          <span v-if="currentPage > 3">...</span>
        </template>
        <button @click="goToPage(currentPage - 1)" v-if="currentPage > 1">{{ currentPage - 1 }}</button>
        <button class="active">{{ currentPage }}</button>
        <button @click="goToPage(currentPage + 1)" v-if="currentPage < totalPages">{{ currentPage + 1 }}</button>
        <template v-if="currentPage < totalPages - 1">
          <span v-if="currentPage < totalPages - 2">...</span>
          <button @click="goToPage(totalPages)">{{ totalPages }}</button>
        </template>
      </span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Следующая</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NewProjectButton from '../components/project/NewProjectButton.vue';
import Project from '../components/project/ProjectComponent.vue';
import { clearAllCookies } from "@/src/js/useCookies";

export default {
  components: {
    NewProjectButton,
    Project,
  },
  data() {
    return {
      projectName: '',
      endDate: '',
      startDate: '',
      selectedStatus: '',
      items: [],
      statuses: [
        { text: 'Готово' },
        { text: 'Опоздание'},
        { text: 'В процессе' },
        { text: 'Все' },
        { text: 'Нет статуса' },
        { text: 'Новый' }
      ],
      currentPage: 1,
    };
  },
  computed: {
    userRole() {
      const user = this.$store.getters.getUser[0];
      return user ? user.role : null;
    },
    itemsPerPage() {
      if (this.currentPage === 1 && (this.userRole === 'Рабочий' || this.userRole === 'Прораб')) {
        return 7;
      }
      return 6;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.items.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
  },
  methods: {
    formatToDateTime(date) {
      return `${date}T00:00:00`;
    },
    async applyFilters() {
      try {
        const params = new URLSearchParams({});

        if (this.endDate) {
          params.append('end_date', this.formatToDateTime(this.endDate));
        }
        if(this.startDate) {
          params.append('start_date', this.formatToDateTime(this.startDate));
        }
        if (this.projectName) {
          params.append('project_name', this.projectName);
        }
        if(this.selectedStatus) {
          params.append('project_status', this.selectedStatus);
        }
        const response = await axios.get(`/api/projects/all/?${params.toString()}`);
        this.items = [
          { type: 'newProjectButton' },
          ...response.data.map(project => ({
            type: 'project',
            name: project.name,
            startDate: this.formatDate(project.start_date),
            endDate: this.formatDate(project.end_date),
            projectPhase: project.status,
            projectId: project.id,
          })),
        ];
        this.currentPage = 1;
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
    async fetchProjects() {
      try {
        const response = await axios.get('/api/projects/all');
        this.items = [
          { type: 'newProjectButton' },
          ...response.data.map(project => ({
            type: 'project',
            name: project.name,
            startDate: this.formatDate(project.start_date),
            endDate: this.formatDate(project.end_date),
            projectPhase: project.status,
            projectId: project.id,
          })),
        ];
        this.currentPage = 1;
      } catch (error) {
        if (error.response.status === 401) {
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
      this.selectedStatus = '';
      this.fetchProjects();
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
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
  beforeMount() {
    this.fetchProjects();
  },
};
</script>

<style scoped>
.content {
  margin-left: 150px;
  padding-top: 60px;
}

.header-search {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  /*padding: 10px 20px;*/
}

.search-input {
  width: 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.filter-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  margin-left: 20px;
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

.projects-container {
  display: flex;
  flex-wrap: wrap;
}

.project-item {
  box-sizing: border-box;
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

.pagination button.active {
  background-color: #5c5583;
}

.pagination button:hover {
  background-color: #5c5583;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>