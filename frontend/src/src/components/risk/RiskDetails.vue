<template>
    <div class="risk-details">
      <h1>Детали риска</h1>
      <div v-if="risk">
        <h2>{{ risk.title }}</h2>
        <p>{{ risk.description }}</p>
      </div>
      <div v-else>
        <p>Риск не найден.</p>
      </div>
      <button @click="goBack">Назад</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        risk: null,
        tasks: [
          { id: 1, title: 'Износ, поломка', description: 'Студенты могут разбить дорогой кафель...' },
          { id: 2, title: 'Задержка в работах', description: 'Из-за санкций некоторые материалы...' },
          // Добавьте дополнительные риски сюда
        ],
      };
    },
    created() {
      const taskId = parseInt(this.$route.params.taskId);
      this.risk = this.tasks.find(task => task.id === taskId);
    },
    methods: {
      goBack() {
        this.$router.push('/project/risks');
      },
    },
  };
  </script>
  
  <style scoped>
  .risk-details {
    padding: 20px;
  }
  
  button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>  