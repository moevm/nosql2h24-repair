<template>
    <div class="chat-page">
      <HeaderComponent />
      <SidebarComponent />
      <main class="content">
        <div class="chat-header">
            <img src="@/assets/icons/avatar.png" alt="Avatar Icon" class="avatar-icon">
          <p class="username">{{ user.username }}</p>
        </div>
        <div class="chat-messages">
          <div v-for="(message, index) in messages" :key="index" class="message" :class="{ 'sent': message.sender === 'me' }">
            <p>{{ message.text }}</p>
          </div>
        </div>
        <div class="chat-input">
          <input
            type="text"
            v-model="newMessage"
            placeholder="Введите сообщение"
            class="message-input"
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage">Отправить</button>
        </div>
      </main>
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
        user: {
          userId: this.$route.params.userId,
          username: 'Пользователь', // Замените на реальные данные
          avatar: 'https://via.placeholder.com/50', // Замените на реальные данные
        },
        messages: [
          { sender: 'me', text: 'Привет!' },
          { sender: 'user', text: 'Привет! Как дела?' },
          // Добавьте больше сообщений по мере необходимости
        ],
        newMessage: '',
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim()) {
          this.messages.push({ sender: 'me', text: this.newMessage });
          this.newMessage = '';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .content {
    margin-left: 150px;
    padding-top: 60px; /* Увеличиваем отступ сверху, чтобы учесть фиксированный заголовок и поле поиска */
  }
  
  .chat-header {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  
  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .username {
    font-weight: bold;
  }
  
  .chat-messages {
    flex-grow: 1;
    padding: 10px;
    overflow-y: auto;
  }
  
  .message {
    padding: 10px;
    margin: 5px 0;
    border-radius: 4px;
    max-width: 70%;
  }
  
  .message.sent {
    background-color: #dcf8c6;
    align-self: flex-end;
  }

  .avatar-icon {
    margin-right: 20px;
  }
  
  .chat-input {
    display: flex;
    align-items: center;
    padding: 10px;
    border-top: 1px solid #ccc;
  }
  
  .message-input {
    flex-grow: 1;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 10px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style> 
