<template>
  <header class="header">
    <div class="left-section">
      <img src="@/assets/icons/avatar.png" alt="Avatar Icon" class="avatar-icon" @click="showUserCard">
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

    <!-- Всплывающая карточка пользователя -->
    <UserCard :user="selectedUser" :showCard="showCard" @close="closeUserCard" />
  </header>
</template>

<script>
import {useCookies} from '@/src/js/useCookies';
import UserCard from './UserCard.vue'; // Импортируйте компонент UserCard
const { getUserName,  } = useCookies();

export default {
  components: {
    UserCard, // Зарегистрируйте компонент UserCard
  },
  data() {
    return {
      userName: getUserName(), // ФИО пользователя
      currentDateTime: new Date().toLocaleString(), // Дата и время, динамически обновляется
      showCard: false,
      selectedUser: null,
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
    showUserCard() {
      const user = this.$store.getters.getUser;
      this.selectedUser = {
        firstName: user[0].firstName,
        lastName: user[0].lastName,
        email: user[0].email,
        role: user[0].role,
        middleName: user[0].middleName,
      };
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
  cursor: pointer;
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