<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="user-search-page">
    <h1>Поиск пользователя</h1>
    <div class="search-filters">
      <input v-model="lastname" placeholder="Фамилия" class="input-field" />
      <input v-model="name" placeholder="Имя" class="input-field" />
      <input v-model="middelname" placeholder="Отчество" class="input-field" />
      <select v-model="selectedRole" class="select-field">
        <option value="">Все должности</option>
        <option value="Рабочий">Рабочий</option>
        <option value="Заказчик">Заказчик</option>
        <option value="Прораб">Прораб</option>
        <option value="Администратор">Администратор</option>
      </select>
      <button @click="searchUsers">Поиск</button>
    </div>

    <!-- Отображаем список пользователей только если хотя бы один фильтр изменен -->
    <div v-for="user in users" :key="user.id" class="user-item">
      <div>
        <p>{{ user.username }}</p>
        <p>Должность - {{ user.role }}</p>
      </div>
      <div class="user-item-actions">
        <button @click="addToContacts(user)">Добавить в задачу</button>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { getProjectId, getStageId,getTaskId } = useCookies();


export default {
  components: {
    HeaderComponent,
    SidebarComponent,
  },
  data() {
    return {
      lastname: '',
      name: '',
      middelname: '',
      selectedRole: '',
      users: [
        // { id: "6731ccd729ebfd89e5eb0b86", name: "Илья", lastname: "Ильичевич", middlename: "Ильич", role: "Администратор" },
      ],
    };
  },
  computed: {
    // Фильтруем пользователей по введенным значениям
  },
  methods: {
    async searchUsers() {
      this.users = [];
      try {
        const params = new URLSearchParams({
        });

        if (this.selectedRole) {
          params.append('role', this.selectedRole);
        }
        if(this.name){
          params.append('name', this.name);
        }
        if (this.middelname) {
          params.append('middlename', this.middelname);
        }
        if(this.lastname){
          params.append('lastname', this.lastname);
        }
        console.log(params.toString());
        console.log(this.lastname);
        console.log(`/api/projects/get_users/${getProjectId()}?${params.toString()}`);
        const response = await axios.get(`/api/projects/get_users/${getProjectId()}?${params.toString()}`);
        console.log("это дата",response.data);
        // this.users.push(response.data);
        this.users = Object.values(response.data).map(user => ({
          username: user.username,
          // lastname: user.lastname,
          // middlename: user.middlename,
          id: user.id,
          role: user.role,
        }));
        console.log(this.users);
      } catch (error) {
        console.error('Ошибка при загрузке контактов:', error);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
    },
    async addToContacts(user) {
      try {
        await axios.put(`/api/tasks/${getProjectId()}/${getStageId()}/${getTaskId()}/${user.id}`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        alert(`Пользователь ${user.username} добавлен в задачу`);
        this.$router.push(`/tasks/viewRedactorTask`);
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
    },
    // searchUsers() {
    //   // Метод для обработки поиска при нажатии кнопки "Поиск"
    //   // Фильтрация выполняется автоматически в computed property `filteredUsers`
    // },
  },
  // beforeMount() {
  //   this.fetchContactData();
  // },
};
</script>

<style scoped>
.user-search-page {
  margin-left: 150px;
  padding-top: 60px;
}

.search-filters {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 20px;
}

.input-field {
  width: 150px;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.input-field:focus {
  border-color: #625b71;
  outline: none;
}

.select-field {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.select-field:focus {
  border-color: #625b71;
  outline: none;
}

.user-item {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-item p {
  margin: 0;
}

.user-item-actions {
  display: flex;
  gap: 10px;
}

.user-item button {
  background-color: #625b71;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-item button:hover {
  background-color: #625b71;
}

.search-filters button {
  background-color: #625b71;
  color: #fff;
  padding: 8px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.search-filters button:hover {
  background-color: #625b71;
  transform: scale(1.05);
}

.search-filters button:active {
  transform: scale(1);
}
</style>
