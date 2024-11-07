<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isRegister ? 'Регистрация' : 'Авторизация' }}</h2>

      <!-- Поле логина -->
      <input
          v-model="email"
          :class="{'input-error': errors.email}"
          type="text"
          placeholder="Логин(email)" />
      <p v-if="errors.email" class="error-message">{{ errors.email }}</p>

      <!-- Поле пароля -->
      <input
          v-model="password"
          :class="{'input-error': errors.password}"
          type="password"
          placeholder="Пароль" />
      <p v-if="errors.password" class="error-message">{{ errors.password }}</p>

      <!-- Дополнительные поля для регистрации -->
      <template v-if="isRegister">
        <input
            v-model="name"
            :class="{'input-error': errors.name}"
            type="text"
            placeholder="Имя" />
        <p v-if="errors.name" class="error-message">{{ errors.name }}</p>

        <input
            v-model="lastname"
            :class="{'input-error': errors.lastname}"
            type="text"
            placeholder="Фамилия" />
        <p v-if="errors.lastname" class="error-message">{{ errors.lastname }}</p>

        <input
            v-model="middlename"
            :class="{'input-error': errors.middlename}"
            type="text"
            placeholder="Отчество" />
        <p v-if="errors.middlename" class="error-message">{{ errors.middlename }}</p>

        <input
            v-model="confirmPassword"
            :class="{'input-error': errors.confirmPassword}"
            type="password"
            placeholder="Повторите пароль" />
        <p v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</p>

        <select
            v-model="role"
            :class="{'input-error': errors.role}">
          <option value="" disabled>Выберите роль</option>
          <option value="Рабочий">Рабочий</option>
          <option value="Заказчик">Заказчик</option>
          <option value="Прораб">Прораб</option>
          <option value="Администратор">Администратор</option>
        </select>
        <p v-if="errors.role" class="error-message">{{ errors.role }}</p>
      </template>

      <!-- Кнопка действия (войти или зарегистрироваться) -->
      <button @click="isRegister ? register() : authenticate()">
        {{ isRegister ? 'Зарегистрироваться' : 'Войти' }}
      </button>

      <!-- Ошибка с сервера -->
      <p v-if="serverError" class="error-message">{{ serverError }}</p>

      <!-- Переключение между авторизацией и регистрацией -->
      <p class="switch-mode" @click="toggleRegister">
        {{ isRegister ? 'Есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрируйся' }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      name: '',
      lastname: '',
      middlename: '',
      confirmPassword: '',
      role: '',
      isRegister: false,
      errors: {}, // Ошибки валидации
      serverError: '', // Ошибка с сервера
    };
  },
  methods: {
    toggleRegister() {
      this.isRegister = !this.isRegister;
      this.errors = {}; // Очищаем ошибки при переключении
      this.serverError = ''; // Очищаем ошибку с сервера при переключении
    },

    validate() {
      this.errors = {}; // Очищаем старые ошибки
      let isValid = true;

      // Проверка для email
      if (!this.email) {
        this.errors.email = 'Email обязателен';
        isValid = false;
      }

      // Проверка для пароля
      if (!this.password) {
        this.errors.password = 'Пароль обязателен';
        isValid = false;
      }

      // Проверка для подтверждения пароля
      if (this.isRegister && this.password !== this.confirmPassword) {
        this.errors.confirmPassword = 'Пароли не совпадают';
        isValid = false;
      }

      // Проверка для остальных полей регистрации
      if (this.isRegister) {
        if (!this.name) {
          this.errors.name = 'Имя обязательно';
          isValid = false;
        }
        if (!this.lastname) {
          this.errors.lastname = 'Фамилия обязательна';
          isValid = false;
        }
        if (!this.middlename) {
          this.errors.middlename = 'Отчество обязательно';
          isValid = false;
        }
        if (!this.role) {
          this.errors.role = 'Роль обязательна';
          isValid = false;
        }
      }

      return isValid;
    },

    async authenticate() {
      if (!this.validate()) return; // Прекращаем выполнение, если есть ошибки валидации

      const dataToSend = {
        email: this.email,
        password: this.password,
      };

      try {
        const res = await axios.post('http://172.18.0.4:8000/api/auth/login', dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
        // Дополнительный код для обработки успешного входа
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.message) {
            this.serverError = error.response.data.message; // Сохраняем ошибку с сервера
          }
        }
      }
    },

    async register() {
      if (!this.validate()) return; // Прекращаем выполнение, если есть ошибки валидации

      const dataToSend = {
        email: this.email,
        name: this.name,
        lastname: this.lastname,
        middlename: this.middlename,
        password: this.password,
        role: this.role,
      };

      try {
        const res = await axios.post('http://172.18.0.4:8000/api/auth/register', dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
        // Дополнительный код для обработки успешной регистрации
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.message) {
            this.serverError = error.response.data.message; // Сохраняем ошибку с сервера
          }
        }
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.auth-box {
  width: 480px;
  padding: 20px;
  background: #ebebeb;
  border-radius: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

input,
select {
  width: 380px;
  height: 36px;
  padding: 8px;
  background: #fcfcfc;
  border: 1px solid #3f3f3f;
  border-radius: 13px;
  box-sizing: border-box;
}

.input-error {
  border-color: red;
}

button {
  width: 380px;
  height: 49px;
  background: #625b71;
  border-radius: 10px;
  font-family: 'Single Day', sans-serif;
  font-size: 16px;
  color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.switch-mode {
  width: 380px;
  font-family: 'Single Day', sans-serif;
  font-size: 16px;
  text-align: center;
  color: #000000;
  cursor: pointer;
  margin-top: 10px;
}

.error-message {
  color: red;
  font-size: 14px;
}
</style>
