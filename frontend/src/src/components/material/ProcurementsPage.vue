<template>
  <div class="main-container">
    <HeaderComponent />
    <ProjectSidebarComponent />

    <div class="content">
      <div class="purchases-container">
        <h1>Ремонт кафедры МОЭВМ</h1>
        <p>Итоговая стоимость: 3,100,000 руб</p>
        
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

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ProcurementsItemComponent,
  },
  data() {
    return {
      searchQuery: '',
      materials: [
        { id: 1, name: 'краска бежевая', quantity: 20, unit: 'банка 5 л.', pricePerUnit: 5000, totalCost: 100000, inStock: true },
        { id: 2, name: 'богемский кафель', quantity: 1500, unit: 'шт', pricePerUnit: 20000, totalCost: 3000000, inStock: false },
        // Добавьте другие материалы здесь
      ],
    };
  },
  computed: {
    filteredMaterials() {
      return this.materials.filter(material => 
        material.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    goToAddMaterial() {
      this.$router.push({ path: '/add-material' });
    },
    viewDetails(materialId) {
      this.$router.push({ path: `/material-details/${materialId}` });
    },
    deleteMaterial(materialId) {
      this.materials = this.materials.filter(material => material.id !== materialId);
    },
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
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  margin-left: auto;
}

.materials-list {
  margin-top: 20px;
}
</style>