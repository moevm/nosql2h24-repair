<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="user-search-page">
    <h1>Данные приложения</h1>
    <div class="header-buttons">
      <button @click="triggerFileInput">Импорт БД</button>
      <input
          type="file"
          ref="fileInput"
          @change="importBD"
          style="display: none;"
      />
      <button @click="exportBD">Экспорт БД</button>
    </div>
    <h1>Просмотр пользователей</h1>
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
      <button @click="resetFilters">Сбросить</button>
    </div>

    <!-- Отображаем список пользователей только если хотя бы один фильтр изменен -->
    <div v-for="user in users" :key="user.id" class="user-item">
      <div @click="showUserCard(user)">
        <p>{{ user.lastname }} {{ user.name }} {{ user.middlename }}</p>
        <p>Должность - {{ user.role }}</p>
      </div>
      <div class="user-item-actions">
        <button @click="goToChat(user)">Перейти в чат</button>
        <!-- <button v-if="userRole === 'Администратор'">Удалить пользователя</button> -->
      </div>
    </div>

    <!-- Всплывающая карточка пользователя -->
    <UserCard :user="selectedUser" :showCard="showCard" @close="closeUserCard" />
  </div>
</template>

<script>
import HeaderComponent from './bars/HeaderComponent.vue';
import SidebarComponent from './bars/SidebarComponent.vue';
import UserCard from './bars/UserCard.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { setReceiverId, setChatName, setChatId } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
    UserCard, // Добавьте новый компонент
  },
  data() {
    return {
      jsonData:[],
      lastname: '',
      name: '',
      middelname: '',
      selectedRole: '',
      users: [],
      showCard: false,
      selectedUser: null,
    };
  },
  computed: {
    userRole() {
      const user = this.$store.getters.getUser[0];
      return user ? user.role : null;
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    async importBD(event) {
      const file = event.target.files[0];
      if (!file) {
        alert("Файл не выбран!");
        return;
      }

      const reader = new FileReader();

      reader.onload = async (e) => {
        try {
          const importedData = JSON.parse(e.target.result);

          // Проверяем наличие поля `users` и его содержимого
          if (!importedData.user || !Array.isArray(importedData.user) || importedData.user.length === 0) {
            throw new Error("Коллекция `user` должна существовать и содержать данные!");
          }

          const formData = new FormData();
          formData.append("file", file);

          // Удаляем `Content-Type` из заголовков, так как браузер сам установит правильный
          try {
            const res = await axios.post(`api/data/import`, formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
              withCredentials: true,
            });
            console.log(res);
            this.showErrors = false;
            alert('Данные успешно импортированы!');
          } catch (error) {
            if (error.response && error.response.status === 401) {
              this.$store.commit('removeUsers'); // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            if (error.response && error.response.status === 400) {
              alert('Бд не пуста');
            }
            console.error("Ошибка сети:", error);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }
        } catch (error) {
          console.error("Ошибка импорта:", error);
          alert(error.message || "Произошла ошибка при импорте данных.");
        }
      };

      reader.onerror = () => {
        alert("Ошибка чтения файла!");
      };

      reader.readAsText(file);
    },
    async exportBD() {
      try {
        const response = await axios.get(`api/data/export/json`);
        this.jsonData = response.data;
      } catch (error) {
        if (error.response?.status === 401) {
          this.$store.commit('removeUsers');
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке контактов:', error);
        if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail;
        }
        return;
      }

      console.log(this.jsonData);

      if (Object.keys(this.jsonData).length > 0) {
        // Преобразуем Proxy в обычный объект, если требуется
        const normalizedData = JSON.parse(JSON.stringify(this.jsonData));

        const json = JSON.stringify(normalizedData, null, 2); // Преобразуем объект в JSON строку
        const blob = new Blob([json], { type: "application/json" }); // Создаём Blob объект
        const url = URL.createObjectURL(blob); // Генерируем URL

        // Создаём временный <a> элемент для скачивания файла
        const link = document.createElement("a");
        link.href = url;
        link.download = `dumpBd.json`; // Имя файла
        document.body.appendChild(link); // Добавляем в DOM, чтобы клик сработал
        link.click(); // Программно кликаем по ссылке
        document.body.removeChild(link); // Удаляем элемент ссылки из DOM

        // Освобождаем память
        URL.revokeObjectURL(url);
      } else {
        alert("У вас нет данных БД, которые можно экспортировать");
      }
    },
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
        const response = await axios.get(`/api/user/find/?${params.toString()}`);
        this.users = Object.values(response.data).map(user => ({
          name: user.name,
          lastname: user.lastname,
          middlename: user.middlename,
          id: user.id,
          role: user.role,
          email: user.email
        }));
      } catch (error) {
        if(error.response.status === 401){
          this.$store.commit('removeUsers');
          clearAllCookies();
          this.$router.push("/login");
        }
        console.error('Ошибка при загрузке контактов:', error);
        if (error.response && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        }
      }
    },
    goToChat(user) {
      setChatName(`${user.lastname} ${user.name} ${user.middlename}`);
      setReceiverId(user.id);
      setChatId("");
      this.$router.push(`/chat`);
    },
    showUserCard(user) {
      this.selectedUser = user;
      this.showCard = true;
    },
    closeUserCard() {
      this.showCard = false;
      this.selectedUser = null;
    },
  },
};
</script>

<style scoped>
.user-search-page {
  margin-left: 150px;
  padding-top: 60px;
}

.header-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 50px;
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
  cursor: pointer;
}

.user-item p {
  margin: 0;
}

.user-item-actions {
  display: flex;
  gap: 10px;
}

.header-buttons button,
.user-item button,
.user-card button {
  background-color: #625b71;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
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
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.search-filters button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.search-filters button:active {
  transform: scale(1);
}
</style>