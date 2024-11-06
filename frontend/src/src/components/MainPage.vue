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
            :projectLocation="item.location"
            :startDate="item.startDate"
            :endDate="item.endDate"
            :projectPhase="item.phase"
            :projectStatus="item.status"
          />
          <NewProjectButton v-if="item.type === 'newProjectButton'" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
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
        {
          type: 'project',
          name: 'Вырастить дерево',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-01-01',
          endDate: '2024-06-01',
          phase: 'Основной этап',
          status: 'В процессе',
        },
        {
          type: 'project',
          name: 'Посадить ребенка',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-02-01',
          endDate: '2024-07-01',
          phase: 'Основной этап',
          status: 'Завершён',
        },
        {
          type: 'project',
          name: 'Проект 42',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-03-01',
          endDate: '2024-08-01',
          phase: 'Основной этап',
          status: 'В процессе',
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