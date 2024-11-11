<template>
    <header class="header">
      <div class="left-section">
        <img src="@/assets/icons/avatar.png" alt="Avatar Icon" class="avatar-icon">
        <div class="user-info">
          <p class="user-name">{{ userName }}</p>
          <div class="icon messages-icon" @click="goToMessages">
            <img src="@/assets/icons/message.png" alt="Messages Icon" class="message-icon">
          </div>
        </div>
      </div>
      <div class="right-section">
        <p class="date-time">{{ currentDateTime }}</p>
      </div>
    </header>
  </template>

  <script>

  export default {
    data() {
      return {
        userName: this.$store.getters.fullName, // ФИО пользователя
        currentDateTime: new Date().toLocaleString(), // Дата и время, динамически обновляется
      };
    },
    created() {
      this.updateDateTime();
    },
    methods: {
      goToMessages() {
        // Логика перехода на страницу сообщений
        this.$router.push('/messages');
      },
      updateDateTime() {
        setInterval(() => {
          this.currentDateTime = new Date().toLocaleString();
        }, 1000);
      },
    }
  };
  </script>

  <style scoped>
  .header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ebebeb;
    padding: 0 20px;
    z-index: 1000;
  }

  .left-section {
    display: flex;
    align-items: center;
  }

  .avatar-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .user-info {
    display: flex;
    align-items: center;
  }

  .user-name {
    font-size: 16px;
    margin-right: 10px;
  }

  .messages-icon {
    cursor: pointer;
  }

  .right-section {
    font-size: 14px;
  }
  </style>
