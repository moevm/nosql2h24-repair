<template>
  <div class="content">
    <div class="header-search">
      <h1>Проекты</h1>
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск проекта"
          class="search-input"
      />
    </div>
    <div class="projects-container">
      <div v-for="(item, index) in filteredItems" :key="index" class="project-item">
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
        <NewProjectButton v-if="item.type === 'newProjectButton' && userRole !== 'Рабочий'" />
      </div>
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
      searchQuery: '',
      items: [
        {
          type: 'newProjectButton',
        },
      ],
    };
  },
  computed: {
    filteredItems() {
      return this.items.filter(item =>
          item.type === 'newProjectButton' ||
          (item.type === 'project' && item.name.toLowerCase().includes(this.searchQuery.toLowerCase()))
      );
    },
    userRole() {
      const user = this.$store.getters.getUser[0];
      return user ? user.role : null;
    },
  },
  methods: {
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
  padding: 10px 20px;
}

.search-input {
  width: 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.projects-container {
  display: flex;
  flex-wrap: wrap;
}

.project-item {
  box-sizing: border-box;
}
</style>
