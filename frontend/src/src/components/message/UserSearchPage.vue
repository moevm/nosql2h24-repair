<template>
    <HeaderComponent />
    <SidebarComponent />
    <div class="user-search-page">
      <h1>Поиск пользователя</h1>
      <div class="search-filters">
        <input v-model="lastName" placeholder="Фамилия" class="input-field" />
        <input v-model="firstName" placeholder="Имя" class="input-field" />
        <input v-model="patronymic" placeholder="Отчество" class="input-field" />
        <select v-model="selectedRole" class="select-field">
          <option value="">Все должности</option>
          <option value="Заказчик">Заказчик</option>
          <option value="Прораб">Прораб</option>
          <option value="Рабочий">Рабочий</option>
        </select>
      </div>
  
      <!-- Отображаем список пользователей только если хотя бы один фильтр изменен -->
      <div v-if="hasFilters" class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-item">
          <div>
            <p>{{ user.lastName }} {{ user.firstName }} {{ user.patronymic }}</p>
            <p>Должность - {{ user.role }}</p>
          </div>
          <div class="user-item-actions">
            <button @click="goToChat(user.id)">Перейти в чат</button>
            <button @click="addToContacts(user.id)">Добавить в контакты</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../bars/HeaderComponent.vue';
  import SidebarComponent from '../bars/SidebarComponent.vue';
  
  export default {
    components: {
      HeaderComponent,
      SidebarComponent,
    },
    data() {
      return {
        lastName: '',
        firstName: '',
        patronymic: '',
        selectedRole: '',
        users: [
          { id: 1, firstName: 'Иван', lastName: 'Сидоров', patronymic: 'Петрович', role: 'Заказчик' },
          { id: 2, firstName: 'Мария', lastName: 'Кузнецова', patronymic: 'Александровна', role: 'Заказчик' },
          { id: 3, firstName: 'Пётр', lastName: 'Иванов', patronymic: 'Сергеевич', role: 'Прораб' },
          { id: 4, firstName: 'Анна', lastName: 'Смирнова', patronymic: 'Николаевна', role: 'Прораб' },
          { id: 5, firstName: 'Алексей', lastName: 'Петров', patronymic: 'Андреевич', role: 'Рабочий' },
          { id: 6, firstName: 'Ольга', lastName: 'Захарова', patronymic: 'Ивановна', role: 'Рабочий' },
        ],
      };
    },
    computed: {
      // Фильтруем пользователей по введенным значениям
      filteredUsers() {
        return this.users.filter(user =>
          (!this.lastName || user.lastName.includes(this.lastName)) &&
          (!this.firstName || user.firstName.includes(this.firstName)) &&
          (!this.patronymic || user.patronymic.includes(this.patronymic)) &&
          (!this.selectedRole || user.role === this.selectedRole)
        );
      },
      // Проверка, были ли изменения в фильтрах
      hasFilters() {
        return this.lastName || this.firstName || this.patronymic || this.selectedRole;
      },
    },
    methods: {
      goToChat(userId) {
        this.$router.push(`/chat/${userId}`);
      },
      addToContacts(userId) {
        alert(`Пользователь ${userId} добавлен в контакты`);
      },
    },
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
    border-color: #007BFF;
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
    border-color: #007BFF;
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
    background-color: #007BFF;
    color: #fff;
    border: none;
    padding: 6px 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .user-item button:hover {
    background-color: #0056b3;
  }
  </style>  