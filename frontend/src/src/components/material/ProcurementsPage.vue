<template>
  <div class="main-container">
    <HeaderComponent />
    <ProjectSidebarComponent/>

    <div class="content">
      <div class="purchases-container">
        <h1>{{projectName}}</h1>
<!--        <p>Итоговая стоимость: 3,100,000 руб</p>-->
        
        <div class="search-add-container">
          <input
            type="text"
            placeholder="Название материала"
            v-model="searchQuery"
            class="search-input"
          />
          <button @click="goToAddMaterial" class="add-button">+ Добавить</button>
        </div>

        <div class="materials-list">
          <ProcurementsItemComponent
            v-for="material in filteredMaterials"
            :key="material.id"
            :material="material"
            @viewDetails="viewDetails"
            @delete="deleteMaterial"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import ProcurementsItemComponent from '../material/ProcurementsItemComponent.vue';
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { getProjectId, getProjectName } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ProcurementsItemComponent,
  },
  data() {
    return {
      projectName: getProjectName(),
      searchQuery: '',
      procurements: [
      ],
    };
  },
  computed: {
    filteredMaterials() {
      return this.procurements.filter(procurement =>
        procurement.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    goToAddMaterial() {
      this.$router.push(`/add_procurement`);
    },
    viewDetails() {
      // this.$router.push({ path: `/material-details/${materialId}` });
    },
    deleteMaterial(materialId) {
      this.materials = this.materials.filter(material => material.id !== materialId);
    },
    async fetchStageData() {
      try {
        const response = await axios.get(`/api/projects/${getProjectId()}/get_procurements`);
        console.log(response.data);
        this.procurements = Object.values(response.data.procurements).map(procurement => ({
          name: procurement.item_name,
          quantity: procurement.quantity,
          unit: procurement.units,
          pricePerUnit: procurement.price,
          totalCost: procurement.cost,
          materialId: procurement.id,
          user: procurement.created_by.username,
          userRole: procurement.created_by.role,
          inStock: procurement.inStock,
        }));
        console.log(this.procurements);
      } catch (error) {
        console.error('Ошибка при загрузке Закупок:', error);
      }
    }
  },
  beforeMount() {
    this.fetchStageData();
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
}

.content {
  display: flex;
  margin-left: 150px;
  padding-top: 60px;
}

.purchases-container {
  flex: 1;
  padding: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-add-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-button {
  margin-top: 10px;
  padding: 10px;
  background-color: #625b71;
  color: white;
  border: none;
  cursor: pointer;
  margin-left: auto;
}

.materials-list {
  margin-top: 20px;
}
</style>