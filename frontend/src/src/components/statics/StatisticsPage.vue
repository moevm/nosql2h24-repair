<template>
  <div class="statistics-page">
    <HeaderComponent />
    <SidebarComponent />
    <div class="content">
      <h1>Статистика</h1>
      <div class="main-content">
        <!-- Графики -->
        <div class="graphs-container">
          <div class="graph" v-if="chartData.length > 0">
            <h2>Текущий график {{selectedStatType ==='risks'? "рисков": "закупок"}}</h2>
            <BarChart :data="chartData" />
          </div>
          <div class="graph" v-if="chartImportData.length > 0">
            <h2>Импортированный график {{importType ==='risks'? "рисков": "закупок"}}</h2>
            <BarChart :data="chartImportData" />
          </div>
        </div>

        <!-- Фильтры и действия -->
        <div class="filters-and-actions">
          <div class="filters">
            <div class="filter-item">
              <label for="statType">Тип статистики</label>
              <select v-model="selectedStatType" id="statType">
                <option value="" disabled>Не выбрано</option>
                <option value="risks">Риски</option>
                <option value="procurements">Закупки</option>
              </select>
            </div>

            <div class="filter-item">
              <label>Проекты</label>
              <div class="dropdown">
                <button class="dropdown-button" @click="toggleDropdown">
                  {{ getSelectedProjectsLabel }}
                </button>
                <div v-if="isDropdownOpen" class="dropdown-menu">
                  <div v-for="project in projects" :key="project.id" class="dropdown-item">
                    <input
                      type="checkbox"
                      :id="'project-' + project.id"
                      :value="project.id"
                      v-model="selectedProjects"
                    />
                    <label :for="'project-' + project.id">{{ project.name }}</label>
                  </div>
                </div>
              </div>
            </div>

            <div class="filter-item">
              <label>Период времени</label>
              <div class="date-filters">
                <label for="startDate">С</label>
                <input type="date" id="startDate" v-model="startDate" />
                <label for="endDate">До</label>
                <input type="date" id="endDate" v-model="endDate" />
              </div>
            </div>
          </div>
          <button class="apply-button" @click="applyFilters">Применить</button>
          <div class="database-actions">
            <input type="file" @change="importData" accept=".json" hidden ref="fileInput" />
            <button class="action-button" @click="triggerImport">Импортировать</button>
            <button class="action-button" @click="exportData">Экспортировать</button>
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "../bars/HeaderComponent.vue";
import SidebarComponent from "../bars/SidebarComponent.vue";
import BarChart from "./BarChart.vue";
import axios from 'axios';
import { clearAllCookies } from "@/src/js/useCookies";

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    BarChart,
  },
  data() {
    return {
      importType:"",
      selectedStatType: "",
      selectedProjects: [],
      startDate: "",
      endDate: "",
      isDropdownOpen: false,
      chartImportData: [],
      chartData: [], // Пустой массив для скрытия графика
      projects: [
        // { id: 1, name: "Проект 1" },
        // { id: 2, name: "Проект 2" },
        // { id: 3, name: "Проект 3" },
      ],
      errorMessage: "",
    };
  },
  computed: {
    getSelectedProjectsLabel() {
      if (this.selectedProjects.length === 0) return "Выберите проекты";
      return `Выбрано (${this.selectedProjects.length})`;
    },
  },
  methods: {

    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    formatToDateTime(date) {
      return `${date}T00:00:00`; // Преобразует в формат `YYYY-MM-DDT00:00:00`
    },
    async applyFilters() {
      this.errorMessage = "";
      // Проверяем, выбраны ли фильтры, и обновляем график
      if (this.selectedStatType && this.selectedProjects.length > 0) {
        const dataToSend = {
          project_ids: this.selectedProjects,
          stat_type: this.selectedStatType,
          ...(this.startDate && { start_date: this.formatToDateTime(this.startDate) }),
          ...(this.endDate && { end_date: this.formatToDateTime(this.endDate) }),
        };
        // console.log(dataToSend);
        try {
          const res = await axios.post(`/api/statistic/get_stat`, dataToSend, {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
          // console.log(res.data);
          this.chartData = Object.entries(res.data).map(([key, value]) => {
            const matchedProject = this.projects.find(project => project.id === key);
            return matchedProject
              ? { label: matchedProject.name, value: value }
              : null;
          }).filter(item => item !== null);
          const allValuesAreZero = this.chartData.every(item => item.value === 0);

          if (allValuesAreZero) {
            this.chartData = []; // Зануляем массив
            this.errorMessage = "В выбранных датах у всех проектов отсутствуют значения. Если хотите посмотреть по всей дате, то оставьте поля с датой пустыми.";
          } else {
            this.errorMessage = ""; // Очищаем сообщение об ошибке
          }

          console.log(this.chartData);
        } catch (error) {
          if (error.response.status === 401) {
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          console.error("Ошибка сети:", error.message);
          if (error.response && error.response.data.detail) {
            this.errorMessage = error.response.data.detail;
          }
        }
        // this.chartData = this.getFilteredData();
      } else {
        alert("Пожалуйста, выберите все фильтры");
      }
    },
    getFilteredData() {
      // Заглушка для демонстрации данных
      return [
        { label: "Проект 1", value: 5 },
        { label: "Проект 2", value: 10 },
        { label: "Проект 3", value: 7 },
      ];
    },
    triggerImport() {
      this.$refs.fileInput.click(); // Триггерим клик по скрытому <input>
    },
    importData(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          console.log("Импорт")
          const jsonData = JSON.parse(e.target.result);
          const typeObject = jsonData.find((item) => item.type);

          if (typeObject) {
            // Присваиваем значение `type` в importType
            this.importType = typeObject.type;

            // Удаляем объект с ключом `type` из данных
            this.chartImportData = jsonData.filter((item) => !item.type);
          }
          console.log(this.chartImportData)
          // Проверка, что это массив объектов с ключами `label` и `value`
          if (this.validateDataFormat(this.chartData)) {
            alert("Данные успешно импортированы!");
            console.log(this.chartImportData)
          } else {
            this.chartImportData = [];
            alert("Ошибка: Неверный формат данных. Ожидается массив объектов с ключами 'label' и 'value'.");
          }
        } catch (error) {
          alert("Ошибка импорта данных: неверный формат файла.");
        }
      };
      reader.readAsText(file);
    },
    validateDataFormat(data) {
      // Проверяем, что это массив
      if (!Array.isArray(data)) {
        return false;
      }

      // Проверяем каждый объект в массиве
      return data.every(
        (item) =>
          typeof item === "object" &&
          item !== null &&
          "label" in item &&
          "value" in item &&
          typeof item.label === "string" &&
          typeof item.value === "number"
      );
    },
    exportData() {
      if (this.chartData.length > 0) {
        this.chartData.push({type:this.selectedStatType});
        const json = JSON.stringify(this.chartData, null, 2); // Преобразуем объект в JSON строку
        const blob = new Blob([json], { type: "application/json" }); // Создаём Blob объект
        const url = URL.createObjectURL(blob); // Генерируем URL

        // Создаём временный <a> элемент для скачивания файла
        const link = document.createElement("a");
        link.href = url;
        link.download = `data_${this.selectedStatType}.json`; // Имя файла
        link.click();
        // Освобождаем память
        URL.revokeObjectURL(url);
      } else {
        alert("У вас нет данных для графика, которые можно экспортировать")
      }

    },
    async fetchProjects() {
      try {
        const response = await axios.get('/api/projects/all');
        this.projects = [
          ...response.data.map(project => ({
            name: project.name,
            id: project.id,
          })),
        ];
        // console.log(this.projects);
      } catch (error) {
        if (error.response.status === 401) {
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
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
.statistics-page {
  display: flex;
  flex-direction: column;
}

.content {
  margin-top: 60px;
  margin-left: 150px;
  padding: 20px;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.graphs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.graph {
  flex: 1 1 45%; /* Flex-grow, flex-shrink, flex-basis */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.graph h2 {
  margin-bottom: 10px;
}

.filters-and-actions {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.filter-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.dropdown {
  position: relative;
}

.dropdown-button,
.filter-item select {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.filter-item input {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  width: 30%;
  text-align: left;
  cursor: pointer;
  margin-right: 10px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 5px 10px;
}

.dropdown-item input {
  margin-right: 10px;
}

.apply-button {
  background-color: #5a4a7f;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.apply-button:hover {
  background-color: #47366a;
}

.database-actions {
  display: flex;
  gap: 10px;
}

.action-button {
  background-color: #5a4a7f;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #47366a;
}

.date-filters {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-filters label {
  margin-right: 5px;
  font-weight: bold;
}

.date-filters input {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}
.error-message {
   color: red;
   font-weight: bold;
   margin-top: 10px;
 }

@media (max-width: 768px) {
  .graphs-container {
    flex-direction: column;
  }

  .graph {
    flex: 1 1 100%; /* Flex-grow, flex-shrink, flex-basis */
  }
}
</style>
