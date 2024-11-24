<template>
    <div class="task-card">
      <h3 class="task-title">Прибить полки</h3>
      <div class="task-field">
        <label>Начало</label>
        <input type="date" v-model="startDate" readonly />
      </div>
      <div class="task-field">
        <label>Конец</label>
        <input type="date" v-model="endDate" readonly />
      </div>
      <div class="task-field">
        <label>Проект</label>
        <input type="text" v-model="projectName" readonly />
      </div>
      <div class="task-field">
        <label>Статус</label>
        <div class="status-dropdown">
          <button @click="toggleDropdown" :style="{ backgroundColor: currentStatus.color }">
            {{ currentStatus.text }}
          </button>
          <ul v-if="dropdownOpen" class="dropdown-menu">
            <li
              v-for="status in statuses"
              :key="status.text"
              :style="{ backgroundColor: status.color }"
              @click="selectStatus(status)"
            >
              {{ status.text }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>  
  
  <script>
  export default {
    data() {
      return {
        startDate: "2024-12-25",
        endDate: "2024-12-25",
        projectName: "Ремонт кафедры МОЗВМ",
        dropdownOpen: false,
        currentStatus: { text: "В процессе", color: "orange" },
        statuses: [
          { text: "-не выбрано-", color: "#e0e0e0" },
          { text: "Готово", color: "green" },
          { text: "Опоздание", color: "red" },
        ],
      };
    },
    methods: {
      toggleDropdown() {
        this.dropdownOpen = !this.dropdownOpen;
      },
      selectStatus(status) {
        this.currentStatus = status;
        this.dropdownOpen = false;
      },
    },
  };
  </script>
  
  <style scoped>
.task-card {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 15px;
  width: 300px;
  font-family: Arial, sans-serif;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.task-title {
  background-color: #6e6b93;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  text-align: center;
}

.task-field {
  margin-bottom: 10px;
}

.task-field label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.task-field input {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f2f2f2; /* Светло-серый фон для readonly полей */
  color: #6e6e6e; /* Темный цвет текста для readonly полей */
  pointer-events: none; /* Отключает кликабельность */
}
.task-field input[readonly] {
  cursor: not-allowed; /* Курсор при наведении на readonly поля */
}

.status-dropdown {
  position: relative;
}

.status-dropdown button {
  width: 100%;
  padding: 10px;
  border: none;
  color: white;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  list-style: none;
  padding: 0;
  margin: 5px 0 0 0;
  z-index: 10;
}

.dropdown-menu li {
  padding: 10px;
  color: white;
  cursor: pointer;
  text-align: center;
}

.dropdown-menu li:hover {
  opacity: 0.8;
}
</style>