<template>
  <div class="main-page">
    <HeaderComponent />
    <SidebarComponent />
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
import SidebarComponent from '../components/bars/SidebarComponent.vue';
import NewProjectButton from '../components/project/NewProjectButton.vue';
import Project from '../components/project/ProjectComponent.vue';

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
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
            startDate: project.start_date,
            endDate: project.end_date,
            projectLocation: project.description,
            projectPhase: project.status,
            // status: ,
          })),
        ];
      } catch (error) {
        console.error('Ошибка при загрузке проектов:', error);
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