<template>
    <div class="task-item">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <button @click="$emit('details')">Подробнее</button>
      <button @click="$emit('delete')">Удалить</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: String,
      description: String,
    },
  };
  </script>
  
  <style scoped>
  .task-item {
    background-color: #f1f1f1;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
  }
  
  button {
    margin: 5px;
    padding: 5px 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>  