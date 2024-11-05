<template>
  <div class="register-container">
    <div class="form-container">
      <h2>Регистрация</h2>
      <form @submit.prevent="register">
        <label>Логин:</label>
        <input type="text" v-model="login" placeholder="Логин" />

        <label>Email:</label>
        <input type="email" v-model="email" placeholder="Email" />

        <label>Телефон:</label>
        <input type="tel" v-model="phone" placeholder="Телефон" />

        <label>Пароль:</label>
        <input type="password" v-model="password" placeholder="Пароль" />

        <label>Повторите пароль:</label>
        <input type="password" v-model="confirmPassword" placeholder="Пароль" />

        <button type="submit">Зарегистрироваться</button>
      </form>
      <p class="login-link">Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    register() {
      // Логика регистрации
      alert('Регистрация прошла успешно!');
    }
  }
};
</script>

<style scoped>
.register-container {
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

.login-link {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}

.login-link a {
  color: #6c5ce7;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
