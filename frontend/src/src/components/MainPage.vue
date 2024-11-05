<template>
  <div class="main-page">
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

    <aside class="sidebar">
      <div v-if="isCustomer" class="menu-item" @click="goToStatistics">
        <img src="@/assets/icons/statics.png" alt="Static Icon" class="static-icon"> 
        <p>Статистика</p>
      </div>
      <div class="menu-item" @click="logOut">
        <img src="@/assets/icons/logout.png" alt="Logout Icon" class="logout-icon">
      </div>
    </aside>

    <main class="content">
      <h1>Проекты</h1>
      <div class="projects-container">
        <Project 
          v-for="(project, index) in projects" 
          :key="index" 
          :projectName="project.name" 
          :projectLocation="project.location" 
          :startDate="project.startDate" 
          :endDate="project.endDate" 
          :projectPhase="project.phase" 
          :projectStatus="project.status" 
        />
      </div>
    </main>
  </div>
</template>

<script>
import Project from '../components/ProjectComponent.vue'; // Путь к вашему компоненту Project

export default {
  components: {
    Project,
  },
  data() {
    return {
      userName: 'Иванов Иван Иванович', // ФИО пользователя
      currentDateTime: new Date().toLocaleString(), // Дата и время, динамически обновляется
      isCustomer: true, // Условие для отображения раздела статистики для заказчика
      projects: [
        {
          name: 'Вырастить дерево',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-01-01',
          endDate: '2024-06-01',
          phase: 'Основной этап',
          status: 'В процессе',
        },
        {
          name: 'Посадить ребенка',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-02-01',
          endDate: '2024-07-01',
          phase: 'Основной этап',
          status: 'Завершён',
        },
        {
          name: 'Проект 42',
          location: 'СПбГЭТУ ЛЭТИ',
          startDate: '2024-03-01',
          endDate: '2024-08-01',
          phase: 'Основной этап',
          status: 'В процессе',
        },
        // Добавьте больше проектов по мере необходимости
      ],
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
    goToStatistics() {
      // Логика перехода на страницу статистики
      this.$router.push('/statistics');
    },
    logOut() {
      // Логика выхода на страницу авторизации
      this.$router.push('/login');
    },
    updateDateTime() {
      setInterval(() => {
        this.currentDateTime = new Date().toLocaleString();
      }, 1000);
    }
  }
};
</script>

<style scoped>
.main-page {
  display: flex;
}

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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.left-section {
  display: flex;
  align-items: center;
}

.avatar {
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

.sidebar {
  width: 100px;
  height: 100vh;
  position: fixed;
  top: 60px;
  left: 0;
  background-color: #f4f4f4;
  padding: 20px;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.menu-item {
  cursor: pointer;
  padding: 10px 0;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column; /* Размещает элементы в столбец */
  align-items: center; /* Центрирует элементы по горизонтали */
  cursor: pointer;
}

.static-icon {
  width: 50px; /* Задайте нужный размер иконки */
  height: 50px; /* Задайте нужный размер иконки */
  margin-bottom: 10px; /* Отступ между иконкой и текстом */
}

.menu-item p {
  margin: 0; /* Убираем отступы у текста */
  font-size: 16px; /* Задайте нужный размер текста */
}

.content {
  margin-left: 200px;
  padding-top: 80px;
}

.projects-container {
  display: flex;
  flex-wrap: wrap; /* Позволяет переносить карточки на следующую строку при переполнении */
  justify-content: space-between; /* Распределяет пространство между элементами */
}
</style>