<template>
  <div class="main-container">
    <HeaderComponent />
    <SidebarComponent/>

    <div class="content">
      <div class="task-container">
        <div class="search-bar">
          <h1>{{projectName}}</h1>
          <div class = "filter-bar">
            <input type="text" placeholder="Название риска" v-model="riskName" class="search-input" />
            <button @click="applyFilters">Применить</button>
            <button @click="resetFilters">Сбросить</button>
          </div>
        </div>

        <!-- Кнопка добавления -->
        <button class="add-button" @click="goToAddTask">+ Добавить</button>
        
        <!-- Список задач -->
        <TaskItemComponent
          v-for="risk in risks"
          :key="risk.riskId"
          :projectId="projectId"
          :projectName="projectName"
          :title="risk.riskName"
          :id="risk.riskId"
          :description="risk.description"
          @delete="deleteTask(risk.riskId)"
          @details="viewDetails(risk.riskId)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import TaskItemComponent from '../risk/TaskItemComponent.vue';

import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId, getProjectName,setRiskId } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    TaskItemComponent,
  },
  data() {
    return {
      projectName: getProjectName(),
      riskName: '',
      risks: [
        // { id: 1, title: 'Износ, поломка', description: 'Студенты могут разбить дорогой кафель. ...' },
        // { id: 2, title: 'Задержка в работах', description: 'Из-за санкций некоторые материалы ...' },
      ],
    };
  },
  computed: {
    // filteredTasks() {
    //   return this.risks.filter(risk =>
    //     risk.riskName.toLowerCase().includes(this.searchQuery.toLowerCase())
    //   );
    // },
  },
  methods: {
    goToAddTask() {
      this.$router.push(`/add_risk`);
    },
    addTask(newRisk) {
      this.risks.push(newRisk);
    },
    deleteTask(id) {
      this.risks = this.risks.filter(risk => risk.riskId !== id);

    },
    viewDetails(id) {
      setRiskId(id);
      console.log("Вызов просмотра риска");
      this.$router.push(`/risk-details`);
    },
    async applyFilters() {
      try {
        const params = new URLSearchParams({
        });
        if (this.riskName) {
          params.append('name', this.riskName);
        }
          const response = await axios.get(`/api/projects/${getProjectId()}/get_risks/?${params.toString()}`);
          console.log(response.data);
          this.risks = Object.values(response.data.risks).map(risk => ({
            riskName: risk.name,
            description: risk.description,
            riskId: risk.id,
          }));
          // console.log(this.risks);
      } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          console.error('Ошибка при загрузке проектов:', error);
      }
    },
    async fetchRisks() {
      try {
        const response = await axios.get(`/api/projects/${getProjectId()}/get_risks`);
        console.log(response.data);
        this.risks = Object.values(response.data.risks).map(risk => ({
          riskName: risk.name,
          description: risk.description,
          riskId: risk.id,
        }));
        // console.log(this.risks);
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке проектов:', error);
      }
    },
    resetFilters() {
      this.riskName ='';
      this.fetchRisks();
    },
  },
  beforeMount() {
    this.fetchRisks();
  }
};
</script>

<style scoped>
/* Основные стили */
.main-container {
  display: flex;
  flex-direction: column;
}

.content {
  display: flex;
  margin-left: 150px;
  padding-top: 30px;
}

/* Стили для верхнего компонента */
header-component {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #f8f8f8;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Стили для бокового меню */
sidebar-component {
  width: 200px;
  background-color: #e8e8e8;
  padding: 15px;
}

/* Стили для основного содержимого */
.task-container {
  flex: 1;
  padding: 20px;
}

.search-bar {
  top: 60px; /* Высота верхнего бара */
  left: 200px; /* Ширина бокового бара */
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
}

.add-button {
  margin-top: 10px;
  padding: 5px 15px;
  background-color: #625b71;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 10px;
}

.task-item {
  background-color: #f1f1f1;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}

.search-input {
  width: 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
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
</style>
