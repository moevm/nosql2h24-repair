<template>
  <div class="project-page">
    <HeaderComponent />
    <ProjectSidebarComponent/>
    <main class="content">
      <div class="main-content">
        <div class="project-description">
          <h2> {{ nameProject }}</h2>
<!--          <p>СПбГЭТУ "ЛЭТИ"</p>-->

          <!-- Описание проекта -->
          <div v-if="isEditing">
            <div
              class="edit-description"
              contenteditable="true"
              v-html="editedDescription"
              @input="updateDescription">
            </div>
            <button @click="saveDescription" class="save-button">Сохранить</button>
            <button @click="cancelEdit" class="cancel-button">Отмена</button>
          </div>
          <div v-else>
            <p>{{ description }}</p>
            <button @click="editDescription" class="edit-button">Редактировать описание</button>
          </div>

        </div>

        <div class="date-selectors">
          <DateSelectorComponent label="Начало" :date="dateStart" />
          <DateSelectorComponent label="Конец" :date="dateEnd" />
        </div>

        <ContactsComponent :contacts="contacts" />
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import DateSelectorComponent from '../project/DateSelectorComponent.vue';
import ContactsComponent from '../project/ContactsComponent.vue';

import { useCookies } from '@/src/js/useCookies';
const { getProjectId } = useCookies();

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    DateSelectorComponent,
    ContactsComponent,
  },
  data() {
    return {
      nameProject: '',
      description: '',
      dateStart:'',
      dateEnd:'',
      contacts:[

      ],
      isEditing: false,
      editedDescription: ''
    };
  },
  created() {
    this.fetchProjectData();
    console.log(this.nameProject)
  },
  methods: {
    editDescription() {
      this.isEditing = true;
      this.editedDescription = this.description;
    },
    saveDescription() {
      this.description = this.editedDescription;
      this.isEditing = false;
    },
    cancelEdit() {
      this.isEditing = false;
    },
    updateDescription(event) {
      this.editedDescription = event.target.innerHTML;
    },
    async fetchProjectData() {
      try {
        const response = await axios.get(`/api/projects/one/${getProjectId()}`);
        this.nameProject = response.data.project.name;
        this.description = response.data.project.description;
        this.dateStart = this.formatDate(response.data.project.created_at);
        this.dateEnd = this.formatDate(response.data.project.end_date);
        this.contacts = Object.values(response.data.project.contacts).map(contact => ({
          userName: contact.username,
          role: contact.role,
        }));
      } catch (error) {
        console.error('Ошибка при загрузке проекта:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы с 0 по 11, поэтому +1
      const year = date.getFullYear();
      return `${day}.${month}.${year}`;
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


.edit-button, .save-button, .cancel-button {
  margin-top: 10px;
  padding: 5px 10px;
  cursor: pointer;
}

.save-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.cancel-button {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  margin-left: 10px;
}

.date-selectors {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.contacts {
  flex: 1;
}
</style>
