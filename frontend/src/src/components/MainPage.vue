<template>
  <div class="main-page">
    <HeaderComponent />
    <StaticSidebarComponent />
    <main class="content">
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
        <div v-for="(item, index) in filteredItems" :key="index">
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
          <NewProjectButton v-if="item.type === 'newProjectButton'" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderComponent from '../components/bars/HeaderComponent.vue';
import StaticSidebarComponent from '../components/bars/StaticSidebarComponent.vue';
import NewProjectButton from '../components/project/NewProjectButton.vue';
import Project from '../components/project/ProjectComponent.vue';

export default {
  components: {
    HeaderComponent,
    StaticSidebarComponent,
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
  },
  methods: {
    async fetchProjects() {
      try {
        const response = await axios.get('/api/projects/all');
        console.log(response.data);
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
  top: 60px;
  left: 200px;
  right: 0;
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
  justify-content: space-between;
}
</style>
