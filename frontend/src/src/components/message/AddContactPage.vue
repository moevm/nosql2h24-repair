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
    <div v-for="user in users" :key="user.id" class="user-item" @click="showUserCard(user)">
      <div>
        <p>{{ user.lastname }} {{ user.name }} {{ user.middlename }}</p>
        <p>Должность - {{ user.role }}</p>
      </div>
      <div class="user-item-actions">
        <button @click.stop="addToContacts(user)">Добавить в контакты</button>
      </div>
    </div>

    <!-- Всплывающая карточка пользователя -->
    <UserCard :user="selectedUser" :showCard="showCard" @close="closeUserCard" />
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import UserCard from '../bars/UserCard.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId} = useCookies();


export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    UserCard,
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
      showCard: false,
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
        if(this.email){
          params.append('email', this.email);
        }
        // console.log(params.toString());
        // console.log(this.lastname);
        // console.log(`/api/user/find/?${params.toString()}`);
        const response = await axios.get(`/api/user/find/?${params.toString()}`);
        // console.log("это дата",response.data);
        // this.users.push(response.data);
        this.users = Object.values(response.data).map(user => ({
          name: user.name,
          lastname: user.lastname,
          middlename: user.middlename,
          id: user.id,
          role: user.role,
          email: user.email
        }));
        // console.log(this.users);
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке контактов:', error);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
    },
    async addToContacts(user) {
      const dataToSend = {
        user_id: user.id,
      };
      console.log(dataToSend.user_id);
      try {
        const res = await axios.post(`/api/projects/${getProjectId()}/add_contact`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
        alert(`Пользователь ${user.lastname} ${user.name} ${user.middlename} добавлен в контакты`);
        this.$router.push(`/project/${getProjectId()}`);
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');  // Изменяем состояние
          clearAllCookies();
          this.$router.push("/login");
        }
        if(error.response.status === 400){
          if (confirm(`Не удалось добавить {user.lastname} ${user.name} ${user.middlename} в контакты. Убедитесь что он уже не добавлен. Хотите вернуться к задаче?`)) {
            this.$router.push(`/project/${getProjectId()}`);
          }
        }
        console.error("Ошибка сети:", error.message);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
    },
    async showUserCard(user) {
      try {
        const response = await axios.get(`/api/user/get_user/${user.id}`);
        this.selectedUser = {
          firstName: response.data.name,
          lastName: response.data.lastname,
          email: response.data.email,
          role: response.data.role,
          middleName: response.data.middlename,
        };
        console.log(this.selectedUser)
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке карточки пользователя:', error);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
      this.showCard = true;
    },
    closeUserCard() {
      this.showCard = false;
      this.selectedUser = null;
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

.user-item{
  cursor: pointer;
}
</style>
