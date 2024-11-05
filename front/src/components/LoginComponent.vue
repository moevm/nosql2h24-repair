<template>
  <div class="login-container">
    <div class="form-container">
      <h2>Вход</h2>
      <form @submit.prevent="login">
        <label>Логин:</label>
        <input type="text" v-model="login" placeholder="Логин" />

        <label>Пароль:</label>
        <input type="password" v-model="password" placeholder="Пароль" />

        <button type="submit">Войти</button>
      </form>
      <p class="register-link">Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login: '',
      password: ''
    };
  },
  methods: {
    // loginexit() {
    //   // Логика входа
    //   alert('Вход выполнен успешно!');
    // }
  }
};
</script>

<style scoped>
/* Аналогичный стиль для страницы входа */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.form-container {
  width: 300px;
  padding: 20px;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

form label {
  display: block;
  font-size: 14px;
  margin-top: 10px;
}

form input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #6c5ce7;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #5a4fcf;
}

.register-link {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}

.register-link a {
  color: #6c5ce7;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
