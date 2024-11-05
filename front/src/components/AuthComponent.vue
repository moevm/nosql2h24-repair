<template>
  <div class="auth">
    <h1>Регистрация</h1>
    <form @submit.prevent="handleSubmit">
      <table>
        <tr>
          <td>Логин:</td>
          <td><input type="text" v-model="login" class="input-field" /></td>
        </tr>
        <tr>
          <td>Email:</td>
          <td><input type="email" v-model="email" class="input-field" /></td>
        </tr>
        <tr>
          <td>Телефон:</td>
          <td><input type="tel" v-model="phone" class="input-field" /></td>
        </tr>
        <tr>
          <td>Роль:</td>
          <td>
            <select v-model="role" class="input-field">
              <option value="Заказчик">Заказчик</option>
              <option value="Рабочий">Рабочий</option>
              <option value="Прораб">Прораб</option>
              <option value="Админ">Админ</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>Пароль:</td>
          <td><input type="password" v-model="password" class="input-field" /></td>
        </tr>
        <tr>
          <td>Повторите пароль:</td>
          <td><input type="password" v-model="confirmPassword" class="input-field" /></td>
        </tr>
      </table>
      <button type="submit" class="register-button">Регистрация</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AuthComponent',
  data() {
    return {
      login: '',
      email: '',
      phone: '',
      role: 'Заказчик',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    handleSubmit() {
      if (this.password !== this.confirmPassword) {
        alert('Пароли не совпадают!');
        return;
      }
      // Здесь можно добавить логику для отправки данных на сервер
      alert('Регистрация успешна!');
    }
  }
};
</script>

<style scoped>
.auth {
  background-color: #FFFFFF;
  padding: 20px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

h1 {
  margin-bottom: 20px;
}

table {
  background-color: #EBEBEB;
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
}

td {
  padding: 10px;
}

.input-field {
  width: 100%;
  padding: 10px;
  background-color: #FCFCFC;
  border: none;
  border-radius: 4px;
}

.register-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #625B71;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #524B61;
}
</style>
