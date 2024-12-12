<template>
  <div class="main-container">
    <HeaderComponent />
    <SidebarComponent/>

    <div class="content">
      <div class="purchases-container">
        <h1>{{ projectName }}</h1>

        <div class="search-add-container">
          <div class="filter-container">
            <div class="date-filter">
              <p>Дата доставки</p>
              <input type="date" v-model="startDate" class="large-input" />
              <span>-</span>
              <input type="date" v-model="endDate" class="large-input" />
            </div>
            <input
              type="text"
              placeholder="Название материала"
              v-model="searchQuery"
              class="search-input"
            />
            <div class="status-filter">
              <label for="status">В наличии</label>
              <select v-model="selectedStatus">
                <option v-for="status in statuses" :key="status" :value="status">
                  {{ status }}
                </option>
              </select>
              <label for="status">Создатель</label>
              <select v-model="selectedStatus">
                <option v-for="role in roles" :key="role" :value="role">
                  {{ role }}
                </option>
              </select>
            </div>
            <button @click="applyFilters">Применить</button>
          </div>
          <button @click="goToAddMaterial" class="add-button">+ Добавить</button>
        </div>

        <div class="materials-list">
          <ProcurementsItemComponent
            v-for="material in filteredMaterials"
            :key="material.materialId"
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
import SidebarComponent from '../bars/SidebarComponent.vue';
import ProcurementsItemComponent from '../material/ProcurementsItemComponent.vue';
import axios from 'axios';
import { clearAllCookies, useCookies } from '@/src/js/useCookies';
const { getProjectId, getProjectName } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    ProcurementsItemComponent,
  },
  data() {
    return {
      projectName: getProjectName(),
      searchQuery: '',
      startDate: '',
      endDate: '',
      selectedStatus: '',
      procurements: [],
      statuses: [
        'Нет',
        'Да',
        'Не выбрано',
      ],
      roles: [
        'Прораб',
        'Администратор',
        'Заказчик',
        'Не выбрано',
      ],
    };
  },
  computed: {
    filteredMaterials() {
      return this.procurements.filter(procurement =>
        procurement.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
        (!this.startDate || new Date(procurement.date) >= new Date(this.startDate)) &&
        (!this.endDate || new Date(procurement.date) <= new Date(this.endDate)) &&
        (!this.selectedStatus || procurement.inStock === this.selectedStatus)
      );
    },
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
    },
    goToAddMaterial() {
      this.$router.push(`/add_procurement`);
    },
    viewDetails() {
      // this.$router.push({ path: `/material-details/${materialId}` });
    },
    deleteMaterial(materialId) {
      this.procurements = this.procurements.filter(material => material.materialId !== materialId);
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
          created_date: this.formatDate(procurement.created_at),
          deliveryDate: this.formatDate(procurement.delivery_date),
          date: procurement.date, // Добавьте поле даты, если оно есть в данных
        }));
        console.log(this.procurements);
      } catch (error) {
        if (error.response.status === 401) {
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке Закупок:', error);
      }
    },
    applyFilters() {
      // Здесь можно добавить дополнительную логику для применения фильтров
    },
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
  padding-top: 30px;
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
  border-radius: 15px;
}

.materials-list {
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
</style>
