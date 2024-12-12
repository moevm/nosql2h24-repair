<template>
  <div class="stages-page">
    <HeaderComponent />
    <SidebarComponent />
    <div class="main-content">
      <div class="stages-container">
        <div class="header-container">
          <!-- Контейнер для заголовка и фильтров -->
          <div class="header-left">
            <h1>{{ projectName }}</h1>
            <!--            <p>СПбГЭТУ "ЛЭТИ"</p>-->
          </div>
          <div class="filter-container">
            <div class="date-filter">
              <input type="date" v-model="startDate" class="large-input" />
              <span>-</span>
              <input type="date" v-model="endDate" class="large-input" />
            </div>
            <input type="text" v-model="search" placeholder="Название этапа" />
            <button @click="applyFilters">Применить</button>
            <button @click="goToAddStagePage" class="add-stage-button">
              Добавить этап
            </button>
          </div>
        </div>

        <StageComponent
          :projectId="projectId"
          :projectName="projectName"
          v-for="stage in filteredStages"
          :key="stage.id"
          :stage="stage"
          @update-stage="updateStage"
          @delete="deleteStage"
          @goToTasks="goToTasks"
        />
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
.stages-page {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.main-content {
  display: flex;
  margin-left: 150px;
  padding-top: 30px;
  width: calc(100% - 150px);
}

.stages-container {
  flex: 1;
  padding: 20px;
}

.header-container {
  display: flex;
  align-items: center; /* Выравниваем элементы по вертикали */
  margin-bottom: 16px;
}

.header-left {
  margin-right: 20px; /* Добавляем отступ между заголовком и фильтрами */
}

.filter-container {
  display: flex;
  align-items: center;
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
}

button:hover {
  background-color: #5c5583;
}

.add-stage-button {
  background-color: #625b71;
  color: white;
  padding: 8px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-left: 10px; /* Добавляем отступ для кнопки */
}

.add-stage-button:hover {
  background-color: #4e4168;
}
</style>
