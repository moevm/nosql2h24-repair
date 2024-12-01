<template>
  <div class="project-page">
    <HeaderComponent />
    <ProjectSidebarComponent/>
    <main class="content">
      <div class="main-content">
        <div class="project-description">
          <h2> {{ nameProject }}</h2>

          <!-- Статус, начало и конец одной строчкой над описанием -->
          <div class="project-info">
            <div class="status-info">
              <label for="status" class="status-label">Статус:</label>
              <span v-if="!isEditing" class="status-value">{{ status }}</span>
              <select v-if="isEditing" v-model="editedStatus" class="status-select">
                <option value="В процессе">В процессе</option>
                <option value="Готово">Готово</option>
                <option value="Новый">Новый</option>
                <option value="Опоздание">Опоздание</option>
                <option value="Нет статуса">Нет статуса</option>
              </select>
            </div>
            <div class="date-info">
              <label for="dateStart" class="date-label">Начало:</label>
              <span v-if="!isEditing" class="date-value">{{ dateStart }}</span>
              <input v-if="isEditing" type="date" v-model="editedDateStart" class="date-input" />
            </div>
            <div class="date-info">
              <label for="dateEnd" class="date-label">Конец:</label>
              <span v-if="!isEditing" class="date-value">{{ dateEnd }}</span>
              <input v-if="isEditing" type="date" v-model="editedDateEnd" class="date-input" />
            </div>
          </div>

          <!-- Описание проекта -->
          <div v-if="isEditing">
            <textarea class="edit-description" v-model="editedDescription"></textarea>
            <div class="edit-buttons">
              <button @click="saveChanges" class="save-button">Сохранить</button>
              <button @click="cancelEdit" class="cancel-button">Отмена</button>
              <button @click="deleteProject" class="delete-button">Удалить проект</button>
            </div>
          </div>
          <div v-else>
            <p>{{ description }}</p>
            <button @click="editProject" class="edit-button">Редактировать</button>
          </div>
        </div>

        <ContactsComponent :contacts="contacts" :isEditing="isEditing"/>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import ContactsComponent from '../project/ContactsComponent.vue';

import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ContactsComponent,
  },
  data() {
    return {
      nameProject: '',
      description: '',
      dateStart:'',
      dateEnd:'',
      contacts:[],
      isEditing: false,
      editedDescription: '',
      status: '',
      editedStatus: '',
      editedDateStart: '',
      editedDateEnd: ''
    };
  },
  created() {
    this.fetchProjectData();
    console.log(this.nameProject)
  },
  methods: {
    formatToDateTime(date) {
      return `${date}T00:00:00`; // Преобразует в формат `YYYY-MM-DDT00:00:00`
    },
    editProject() {
      this.isEditing = true;
      this.editedDescription = this.description;
      this.editedStatus = this.status;
      this.editedDateStart = this.dateStart;
      this.editedDateEnd = this.dateEnd;
    },
    async saveChanges() {
      this.description = this.editedDescription;
      this.status = this.editedStatus;
      this.dateStart = this.editedDateStart;
      this.dateEnd = this.editedDateEnd;
      this.isEditing = false;
      console.log(this.description);
      const dataToSend = {
        description:this.description,
        status:this.status,
        start_date: this.formatToDateTime(this.dateStart),
        end_date: this.formatToDateTime(this.dateEnd)
      };
      console.log(dataToSend)
      try {
        const res = await axios.put(`/api/projects/update/${getProjectId()}`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }
    },
    cancelEdit() {
      this.isEditing = false;
    },
    async deleteProject() {
      try {
        const res = await axios.delete(`/api/projects/delete/${getProjectId()}`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
        this.$router.push('/projects'); // Переход на страницу списка проектов после удаления
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }
    },
    async fetchProjectData() {
      try {
        const response = await axios.get(`/api/projects/one/${getProjectId()}`);
        this.nameProject = response.data.project.name;
        this.description = response.data.project.description;
        this.dateStart = this.formatDate(response.data.project.created_at);
        this.dateEnd = this.formatDate(response.data.project.end_date);
        this.status = response.data.project.status || 'Нет статуса';
        this.contacts = Object.entries(response.data.project.contacts).map(([id, contact]) => ({
          id, // ID пользователя (ключ объекта)
          userName: contact.username,
          role: contact.role,
        }));
        console.log(this.contacts);
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error(error.response.status);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${year}-${month}-${day}`; // Формат YYYY-MM-DD для input type="date"
    },
  },
};
</script>

<style scoped>
.content {
  margin-left: 150px;
  padding-top: 60px;
}

.main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  gap: 20px;
}

.project-description {
  flex: 2;
  overflow-y: auto;
  padding-right: 10px;
  width: 900px;
  display: flex;
  flex-direction: column;
}

.project-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.status-info, .date-info {
  display: flex;
  align-items: center;
}

.status-label, .date-label {
  margin-right: 10px;
  font-weight: bold;
}

.status-value, .date-value {
  display: inline-block;
  padding: 5px 10px;
  border: 2px solid;
  border-radius: 4px;
  background-color: #f0f0f0;
}

.status-select, .date-input {
  width: 150px;
  padding: 8px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.edit-description {
  width: 100%;
  padding: 10px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 150px;
  resize: none;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: hidden;
  overflow-y: auto;
  box-sizing: border-box;
}

.edit-button, .save-button, .cancel-button, .delete-button {
  margin-top: 10px;
  padding: 10px 15px;
  cursor: pointer;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 20px; /* Rounded corners */
}

.save-button {
  margin-right: 10px;
}

.cancel-button {
  margin-right: 10px;
}

.contacts {
  flex: 1;
}

.edit-buttons {
  display: flex;
  align-items: center;
  margin-top: 10px;
}
</style>
