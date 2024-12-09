<template>
  <HeaderComponent />
  <SidebarComponent />
  <div class="chat-container">
    <header class="chat-header">
      <button class="back-button" @click="goBack">Назад</button>
      <div class="contact-name">{{chatName}}</div>
    </header>

    <div class="messages">
      <div
          v-for="(message, index) in sortedMessages"
          :key="index"
          :class="['message-container', message.sender === 'self' ? 'right' : 'left']"
      >
        <div :class="['message', message.sender === 'self' ? 'self-message' : '']">
          <p>{{ message.text }}</p>
          <span :class="['timestamp', message.sender === 'self' ? 'self-timestamp' : '']">{{ formatDate(message.date) }}</span>
          <span v-if="message.status === 'read'" class="status-check">✔</span>
        </div>
      </div>
    </div>

    <footer class="chat-footer">
      <input
          type="text"
          placeholder="Введите текст сообщения..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">➤</button>
    </footer>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getReceiverId, getChatName,getChatId,getUserId } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
  },
  data() {
    return {
      chatName: getChatName(),
      chatId: '',
      newMessage: '',
      errorMessage: '',
      messages: [
      ],
      socket: null
    };
  },
  computed: {
    sortedMessages() {
      return [...this.messages].sort((a, b) => new Date(a.date) - new Date(b.date));
    }
  },
  methods: {
    async connectWebSocket() {
      if (!this.chatId) return;

      this.socket = new WebSocket(`ws://localhost:8080/api/message/chat/${this.chatId}`); // Замените на ваш WebSocket URL
      this.socket.onopen = () => console.log('WebSocket соединение установлено');  // Логируем успешное подключение
      this.socket.onopen = () => {
        console.log("WebSocket подключен.");
      };

      this.socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("hfghfh");
        // Обновляем сообщения
        this.messages.push({
          text: message.content,
          date: message.timestamp,
          status: message.status,
          sender: message.sender === getUserId() ? "self" : "other",
        });

        this.$nextTick(() => this.scrollToBottom());
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket ошибка:", error);
      };

      this.socket.onclose = () => {
        console.log("WebSocket отключен.");
        setTimeout(() => {
          // Попытка переподключения
          this.connectWebSocket();
        }, 5000);
      };
    },
    async fetchChat() {
      this.chatId = getChatId();
      if(!this.chatId){
        try {
          const response = await axios.get(`/api/message/check_chat/${getReceiverId()}`);
          if(response.data){
            this.chatId = response.data.id;
          }
        } catch (error) {
          this.errorMessage = error;
          console.error('Ошибка при загрузке чата:', error);
        }
      }
      if(this.chatId) {
        try {
          const response = await axios.get(`/api/message/get_messages/${this.chatId}`);
          console.log(response.data);
          this.messages = Object.values(response.data).map(message => ({
            text: message.content,
              date: message.timestamp,
              status: message.status,
              sender: message.sender === getUserId() ? "self" : "other"
          }));
          console.log("вызываю сокет");
          await this.connectWebSocket(); // Подключаем WebSocket после загрузки чата
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          this.errorMessage = error;
          console.error('Ошибка при загрузке чата:', error);
        }

      }
    },
    async sendMessage() {
      if(!this.chatId){
        if (this.messages.length === 0) {
          const dataToSend = {
            id_receiver: getReceiverId(),
            content: this.newMessage
          };
          this.newMessage = "";
          // console.log(this.messages.length);
          try {
            const res = await axios.post(`/api/message/create_chat`, dataToSend, {
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            // console.log(res.data.id);
            if(res.data.id){
              this.chatId = res.data.id;
              this.messages.push({
                text: res.data.lastMessage.content,
                date: res.data.lastMessage.timestamp,
                status: res.data.lastMessage.status,
                sender: res.data.lastMessage.sender === getUserId() ? "self" : "other"
              });
            }
          } catch (error) {
            if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            this.errorMessage = error;
            console.error("Ошибка сети:", error.message);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }
        }
      }
      else{
        if (this.newMessage.trim() !== "") {
          const dataToSend = {
            chatId: this.chatId,
            receiver: getReceiverId(),
            content: this.newMessage
          };
          this.newMessage = "";
          // console.log(dataToSend);
          try {
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
              this.socket.send(JSON.stringify(dataToSend));
            }
            const res = await axios.post(`/api/message/create_message`, dataToSend, {
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            this.messages.push({
              text: res.data.content,
              date: res.data.timestamp,
              sender: res.data.sender === getUserId() ? "self" : "other",
              status: res.data.status,
            });
          } catch (error) {
            if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
            this.errorMessage = error;
            console.error("Ошибка сети:", error.message);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }
        }
      }
    },
    formatDate(date) {
      const options = { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" };
      return new Date(date).toLocaleString("ru-RU", options);
    },
    goBack(){
      this.$router.push('/messages');
    },
  },
  beforeMount() {
    this.fetchChat();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: 0 auto;
  margin-top: 70px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

.chat-header {
  display: flex;
  padding: 10px;
  background-color: #e9e9e9;
  text-align: center;
  font-weight: bold;
}

.contact-name {
  flex: 1;
  text-align: center;
  font-size: 1.1em;
}

.back-button {
  background-color: #7161ef;
  border: none;
  color: white;
  font-size: 1em;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: auto;
}

.messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.message-container {
  display: flex;
  margin-bottom: 10px;
}

.message-container.left {
  justify-content: flex-start;
}

.message-container.right {
  justify-content: flex-end;
}

.message {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  position: relative;
  background-color: #e0e0e0;
}

.message-container.right .message {
  background-color: #7161ef;
  color: white;
}

.self-message {
  background-color: #7161ef;
  color: white;
}

.timestamp {
  font-size: 0.8em;
  color: gray;
  margin-top: 5px;
  display: block;
}

.self-timestamp {
  color: white;
}

.status-check {
  font-size: 0.8em;
  color: #4caf50;
  margin-left: 5px;
}

.chat-footer {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #e9e9e9;
  border-top: 1px solid #ddd;
}

.chat-footer input[type="text"] {
  flex: 1;
  padding: 8px;
  border-radius: 20px;
  border: 1px solid #ddd;
  outline: none;
}

.chat-footer button {
  background-color: #7161ef;
  border: none;
  color: white;
  font-size: 1.2em;
  padding: 8px 12px;
  margin-left: 10px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
