<template>
  <div class="contacts">
    <div class="contacts-header">
      <h3>Контакты</h3>
      <button v-if="isEditing" @click="addContact" class="add-button">Добавить</button>
    </div>
    <ul>
      <li v-for="contact in contacts" :key="contact.userName">
        <img :src="require(`@/assets/icons/avatar.png`)" alt="Avatar Icon" class="contact-avatar">
        <div class="contact-info">
          <div>{{ contact.userName }}</div>
          <span>{{ contact.role }}</span>
        </div>
        <button v-if="isEditing" @click="deleteContact(contact)" class="delete-button">
          <img :src="require(`@/assets/icons/delete_person.png`)" alt="Delete Icon" class="delete-icon">
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import router from "@/src/router";
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId,getStageId,getTaskId} = useCookies();

export default {
  props: {
    contacts: {
      type: Array,
      required: true
    },
    isEditing: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    addContact() {
      if (this.$route.path.startsWith('/project/')) {
        router.push(`/add_contact`);
        console.log('Добавить контакт');
      }
      if(this.$route.path === '/tasks/viewRedactorTask') {
        router.push(`/add_worker`);
      }
      if(this.$route.path === '/add_task') {
        router.push(`/add_new_worker`);
      }
    },
    async deleteContact(contact) {
      if(this.$route.path === '/tasks/viewRedactorTask') {
        if (confirm(`Удалить рабочего "${contact.userName}"?`)) {
          try {
            await axios.delete(`/api/tasks/${getProjectId()}/${getStageId()}/${getTaskId()}/${contact.id}`, {
              headers: {
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            this.$emit('delete', contact.id);
          } catch (error) {
            if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            // Обработка ошибки, если нужно
            console.error(error);
          }
        }
      }
      if (this.$route.path.startsWith('/project/')) {
        if (confirm(`Удалить контакта "${contact.userName}"?`)) {
          try {
            await axios.delete(`/api/projects/${getProjectId()}/delete_contact/${contact.id}`, {
              headers: {
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            this.$emit('delete', contact.id);
          } catch (error) {
            if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            // Обработка ошибки, если нужно
            console.error(error);
          }
        }
      }
    }
  },
};
</script>

<style scoped>
.contacts {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  width: 200px;
}

.contacts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-button {
  background-color: #625b71;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 10px;
}

.contacts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.contacts li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.contact-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.contact-info {
  display: flex;
  flex-direction: column;
}

.delete-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 5px;
  margin-left: 10px;
}

.delete-icon {
  width: 30px;
  height: 30px;
}
</style>