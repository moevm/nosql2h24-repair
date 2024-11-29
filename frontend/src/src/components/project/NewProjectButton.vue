<template>
    <div class="create-project-button" @click="createProject">
      <h2 class="button-title">Создать проект</h2>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      createProject() {
        // Логика создания проекта
        this.$router.push('/new-project');
      },
    },
  };
  </script>
  
  <style scoped>
  .create-project-button {
    width: 500px; /* Ширина, соответствующая компоненту проекта */
    height: 350px; /* Высота, соответствующая компоненту проекта */
    background-color: #625b71; /* Фоновый цвет кнопки */
    color: white; /* Цвет текста */
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 5px; /* Отступы между карточками проекта */
    display: flex;
    align-items: center; /* Центрирует текст по вертикали */
    justify-content: center; /* Центрирует текст по горизонтали */
    cursor: pointer;
    font-size: 20px; /* Размер текста */
    font-weight: bold; /* Жирность текста */
    text-align: center; /* Выравнивание текста по центру */
  }
  
  .create-project-button:hover {
    background-color: #615b6d; /* Цвет кнопки при наведении */
  }
  </style>
  