<template>
    <div class="messages-page">
      <HeaderComponent />
      <SidebarComponent />
      <main class="content">
        <div class="header-search">
          <h1>Сообщения</h1>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск пользователя"
            class="search-input"
          />
          <button v-if="$route.path !== '/user-search'" @click="goToUserSearch">Поиск пользователя</button>
        </div>
        <div class="chats-container">
          <div v-for="chat in chats" :key="chat.chatId" class="chat-item" @click="goToChat(chat)">
            <img src="@/assets/icons/avatar.png" alt="Avatar Icon" class="avatar-icon">
            <div class="chat-info">
              <p class="username">{{ chat.name }}</p>
              <p class="last-message">{{ chat.lastmessage }}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import HeaderComponent from '../bars/HeaderComponent.vue';
  import SidebarComponent from '../bars/SidebarComponent.vue';
  import axios from 'axios';
  import {clearAllCookies, useCookies} from '@/src/js/useCookies';
  const { getUserId,setChatId,setChatName,setReceiverId } = useCookies();
  export default {
    components: {
      HeaderComponent,
      SidebarComponent,
    },
    data() {
      return {
        searchQuery: '',
        chats: [
        ],
      };
    },
    methods: {
      goToChat(user) {
        setChatName(user.name);
        setReceiverId(user.receiverId);
        setChatId(user.chatId);
        console.log(user.chatId);
        this.$router.push(`/chat`);
      },
      goToUserSearch() {
        this.$router.push('/user-search');
      },
      async fetchChats() {
        try {
          const response = await axios.get('/api/message/get_chats');
          console.log(response.data);
          this.chats = await Promise.all(
              Object.values(response.data).map(async (chat) => {
                // Получаем идентификатор другого участника, исключая текущего пользователя
                const otherUserId = Object.keys(chat.participants).find(id => id !== getUserId());
                const name = chat.participants[otherUserId].name;

                return {
                  receiverId: otherUserId,
                  name: name,
                  lastmessage: chat.lastMessage.content,
                  chatId: chat.id,
                };
              })
          );
          console.log(this.chats);
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          console.error('Ошибка при загрузке чатов:', error);
        }
      },
    },
    beforeMount() {
      this.fetchChats();
    },
  };
  </script>
  
  <style scoped>
  .content {
    margin-left: 150px;
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

  button {
  padding: 8px 12px;
  background-color: #625b71;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  margin-right: 15px;
}

button:hover {
  background-color: #4f416d;
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
