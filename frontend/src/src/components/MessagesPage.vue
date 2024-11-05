<template>
    <div class="messages-page">
      <HeaderComponent />
      <main class="content">
        <div class="header-search">
          <h1>Сообщения</h1>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск пользователя"
            class="search-input"
          />
        </div>
        <div class="chats-container">
          <div v-for="(chat, index) in filteredChats" :key="index" class="chat-item" @click="goToChat(chat.userId)">
            <img src="@/assets/icons/avatar.png" alt="Avatar Icon" class="avatar-icon">
            <div class="chat-info">
              <p class="username">{{ chat.username }}</p>
              <p class="last-message">{{ chat.lastMessage }}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../components/HeaderComponent.vue';
  
  export default {
    components: {
      HeaderComponent,
    },
    data() {
      return {
        searchQuery: '',
        chats: [
          {
            userId: 1,
            username: 'Пользователь 1',
            avatar: 'https://via.placeholder.com/50',
            lastMessage: 'Привет!',
          },
          {
            userId: 2,
            username: 'Пользователь 2',
            avatar: 'https://via.placeholder.com/50',
            lastMessage: 'Как дела?',
          },
          // Добавьте больше чатов по мере необходимости
        ],
      };
    },
    computed: {
      filteredChats() {
        return this.chats.filter(chat =>
          chat.username.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
    },
    methods: {
      goToChat(userId) {
        this.$router.push(`/chat/${userId}`);
      },
    },
  };
  </script>
  
  <style scoped>
  .content {
    margin-left: 50px;
    padding-top: 60px; /* Увеличиваем отступ сверху, чтобы учесть фиксированный заголовок и поле поиска */
  }
  
  .avatar-icon {
    margin-right: 20px;
  }
  
  .header-search {
    top: 60px; /* Высота верхнего бара */
    left: 200px;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    padding: 10px 20px;
  }
  
  .search-input {
    width: 300px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .chats-container {
    display: flex;
    flex-direction: column;
  }
  
  .chat-item {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;
    cursor: pointer;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .chat-info {
    display: flex;
    flex-direction: column;
  }
  
  .username {
    font-weight: bold;
  }
  
  .last-message {
    color: #777;
  }
  </style>  