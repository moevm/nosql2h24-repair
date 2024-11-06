<template>
    <div class="contacts">
      <h3>Контакты</h3>
      <ul>
        <li v-for="contact in contacts" :key="contact.name">
          <img :src="require(`@/assets/icons/avatar.png`)" alt="Avatar Icon" class="contact-avatar">
          <div class="contact-info">
            <div>{{ contact.name }}</div>
            <span>{{ contact.role }}</span>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        contacts: [
          { name: 'Каримов С. Н.', role: 'Прораб', avatar: 'avatar1.png' },
          { name: 'Каримов С. Н.', role: 'Заказчик', avatar: 'avatar2.png' },
          { name: 'Каримов С. Н.', role: 'Работник', avatar: 'avatar3.png' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .contacts {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 8px;
    width: 200px;
  }
  
  .contacts ul {
    list-style: none; /* Убираем точки списка */
    padding: 0;
    margin: 0;
  }
  
  .contacts li {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .contact-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .contact-info {
    display: flex;
    flex-direction: column;
  }
  </style>   