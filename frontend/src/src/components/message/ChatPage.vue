<template>
  <div class="chat-container">
    <header class="chat-header">
      <div class="contact-name">Иванов И.</div>
    </header>

    <div class="messages">
      <div
          v-for="(message, index) in sortedMessages"
          :key="index"
          :class="['message-container', message.sender === 'self' ? 'right' : 'left']"
      >
        <div :class="['message', message.sender === 'self' ? 'self-message' : '']">
          <p>{{ message.text }}</p>
          <span class="timestamp">{{ formatDate(message.date) }}</span>
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
export default {
  data() {
    return {
      newMessage: "",
      messages: [
        {
          text: "Как обстоят дела с ремонтом, когда завершите?",
          date: new Date("2024-10-03T21:37:00"),
          sender: "other",
          status: "read"
        },
        {
          text: "Работаем, но возникли задержки с поставками материалов. Без них продолжить не можем.",
          date: new Date("2024-10-03T21:38:00"),
          sender: "self",
          status: "read"
        },
        {
          text: "Опять? Это уже третья неделя идёт!",
          date: new Date("2024-10-03T21:39:00"),
          sender: "other",
          status: "read"
        },
        {
          text: "К сожалению, задержки по вине поставщика. Мы делаем всё возможное на нашем уровне.",
          date: new Date("2024-10-03T21:40:00"),
          sender: "self",
          status: "read"
        },
        {
          text: "Хорошо, но постарайтесь уложиться в сроки. Ещё неделя – и начнутся проблемы.",
          date: new Date("2024-10-03T21:41:00"),
          sender: "other",
          status: "read"
        },
        {
          text: "Приложим максимум усилий, однако если материалы вновь задержатся, это не будет зависеть от нас.",
          date: new Date("2024-10-03T21:42:00"),
          sender: "self",
          status: "unread"
        }
      ]
    };
  },
  computed: {
    sortedMessages() {
      return [...this.messages].sort((a, b) => new Date(a.date) - new Date(b.date));
    }
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        // Добавляем новое сообщение в массив messages
        this.messages.push({
          text: this.newMessage,
          date: new Date(),
          sender: "self",
          status: "unread"
        });
        this.newMessage = "";
      }
    },
    formatDate(date) {
      const options = { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" };
      return new Date(date).toLocaleString("ru-RU", options);
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f9f9f9;
}

.chat-header {
  padding: 10px;
  background-color: #e9e9e9;
  text-align: center;
  font-weight: bold;
}

.contact-name {
  font-size: 1.1em;
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
