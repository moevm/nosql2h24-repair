<template>
  <div class="task-container">
    <div class="task-card">
      <h3 class="task-title">{{ name }}</h3>
      <div class="task-field">
        <label>Описание</label>
        <div class="description-text">{{ description }}</div>
      </div>
      <div class="task-field">
        <label>Начало</label>
        <div class="date-text">{{ startDate }}</div>
      </div>
      <div class="task-field">
        <label>Конец</label>
        <div class="date-text">{{ endDate }}</div>
      </div>
      <div class="task-field">
        <label>Проект</label>
        <div class="project-text">{{ projectName }}</div>
      </div>
      <div class="task-field">
        <label>Статус</label>
        <div class="status-dropdown">
          <button @click="toggleDropdown" :style="{ backgroundColor: statuses[currentStatus] }">
            {{ currentStatus }}
          </button>
          <ul v-if="dropdownOpen" class="dropdown-menu">
            <li
              v-for="(color, text) in statuses"
              :key="text"
              :style="{ backgroundColor: color }"
              @click="selectStatus(text)"
            >
              {{ text }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- Добавьте другие карточки здесь -->
  </div>
</template>

<script>
import axios from 'axios';
import { clearAllCookies } from "@/src/js/useCookies";

export default {
  props: {
    description: {
      type: String,
      required: true,
    },
    endDate: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    startDate: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      default: 'Нет статуса',
    },
    projectName: {
      type: String,
      default: "Нет в бд"
    },
    id: {
      type: String,
      required: true,
    },
    stageId: {
      type: String,
      required: true,
    },
    projectId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      dropdownOpen: false,
      currentStatus: this.status,
      statuses: {
        "Нет статуса": "#e0e0e0",
        "Готово": "green",
        "Опоздание": "red",
        "В процессе": "orange"
      }
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async selectStatus(status) {
      const dataToSend = {
        status: status,
      };
      try {
        await axios.put(`/api/tasks/update_status_task/${this.projectId}/${this.stageId}/${this.id}`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
      } catch (error) {
        if (error.response.status === 401) {
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }
      this.currentStatus = status;
      this.dropdownOpen = false;
    },
  },
};
</script>

<style scoped>
.task-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* Уменьшите это значение для уменьшения расстояния между карточками */
}

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
  white-space: normal;
  word-wrap: break-word;
}

.task-field {
  margin-bottom: 10px;
}

.task-field label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.description-text, .project-text, .date-text {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f2f2f2; /* Светло-серый фон */
  color: #6e6e6e; /* Темный цвет текста */
  white-space: pre-wrap; /* Перенос текста по словам */
  word-wrap: break-word; /* Перенос длинных слов */
  overflow: hidden; /* Скрывает переполнение */
  text-overflow: ellipsis; /* Добавляет многоточие, если текст не влезает */
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
