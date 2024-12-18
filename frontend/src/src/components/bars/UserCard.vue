<template>
    <div v-if="showCard" class="user-card-overlay" @click="closeUserCard"></div>
    <div v-if="showCard" class="user-card">
      <div class="user-card-content">
        <p>Фамилия: {{ user.lastname }}</p>
        <p>Имя: {{ user.name }}</p>
        <p>Отчество: {{ user.middlename }}</p>
        <p>E-mail: {{ user.email }}</p>
        <p>Должность: {{ user.role }}</p>
      </div>
      <button @click="closeUserCard">Назад</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
      showCard: {
        type: Boolean,
        required: true,
      },
    },
    methods: {
      closeUserCard() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .user-card {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }
  
  .user-card-content {
    text-align: left;
    margin-left: 10px;
  }
  
  .user-card button {
    background-color: #625b71;
    color: #fff;
    border: none;
    padding: 6px 12px;
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.3s;
    text-align: center;
    margin-top: 20px;
  }
  
  .user-card-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }
  </style>  