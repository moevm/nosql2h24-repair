<template>
  <div class="contacts">
    <div class="contacts-header">
      <h3>Контакты</h3>
      <button @click="addContact" class="add-button">Добавить</button>
    </div>
    <ul>
      <li v-for="contact in contacts" :key="contact.userName">
        <img :src="require(`@/assets/icons/avatar.png`)" alt="Avatar Icon" class="contact-avatar">
        <div class="contact-info">
          <div>{{ contact.userName }}</div>
          <span>{{ contact.role }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import router from "@/src/router";

export default {
  props: {
    contacts: {
      type: Array,
      required: true
    }
  },
  methods: {
    addContact() {
      router.push(`/add_contact`);
      console.log('Добавить контакт');
    },
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

.contacts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}

.contacts ul {
  list-style: none;
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
