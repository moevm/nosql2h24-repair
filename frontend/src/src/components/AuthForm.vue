<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isRegister ? 'Регистрация' : 'Авторизация' }}</h2>

      <!-- Поле логина -->
      <input v-model="login" type="text" placeholder="Логин" />

      <!-- Поле пароля -->
      <input v-model="password" type="password" placeholder="Пароль" />

      <!-- Дополнительные поля для регистрации -->
      <template v-if="isRegister">
        <input v-model="email" type="email" placeholder="Email" />
        <input v-model="phone" type="tel" placeholder="Телефон" />
        <input v-model="confirmPassword" type="password" placeholder="Повторите пароль" />
        <select v-model="role">
          <option value="" disabled>Выберите роль</option>
          <option value="worker">Рабочий</option>
          <option value="customer">Заказчик</option>
          <option value="foreman">Прораб</option>
          <option value="admin">Админ</option>
        </select>
      </template>

      <!-- Кнопка действия (войти или зарегистрироваться) -->
      <button @click="isRegister ? register() : authenticate()">
        {{ isRegister ? 'Зарегистрироваться' : 'Войти' }}
      </button>

      <!-- Переключение между авторизацией и регистрацией -->
      <p class="switch-mode" @click="toggleRegister">
        {{ isRegister ? 'Есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрируйся' }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      login: '',
      password: '',
      email: '',
      phone: '',
      confirmPassword: '',
      role: '',
      isRegister: false, // Определяет, находимся ли мы на странице регистрации или авторизации
    };
  },
  methods: {
    toggleRegister() {
      this.isRegister = !this.isRegister;
    },
    async authenticate() {
      // Логика авторизации
      axios.post('http://app-backend:8000/api/auth/login')
          .then(res => {
            console.log(res);
          })
          .catch(error => {
            console.error("Ошибка сети:", error.message);
            if (error.response) {
              console.error("Данные ответа:", error.response.data);
            } else if (error.request) {
              console.error("Запрос:", error.request);
            } else {
              console.error("Сообщение об ошибке:", error.message);
            }
          });
      console.log("authenticate что-то получила");
      // if (this.login === 'user' && this.password === 'password') {
      //   // Успешная авторизация
      //   this.$router.push('/main'); // Переход на основную страницу
      // } else {
      //   alert('Неверный логин или пароль');
      // }
    },
    register() {
      this.sendDataRegistration()
      console.log("registration что-то получила");
      // // Проверки перед регистрацией
      // if (this.password !== this.confirmPassword) {
      //   alert('Пароли не совпадают');
      //   return;
      // }
      // if (!this.login || !this.email || !this.phone || !this.role) {
      //   alert('Заполните все поля');
      //   return;
      // }
      //
      // // Успешная регистрация
      // alert('Регистрация прошла успешно');
      // this.isRegister = false; // Возвращаемся к форме авторизации после успешной регистрации
    },
    async sendDataRegistration() {
      // Формируем JSON-объект
      const dataToSend = {
        login: this.login,
        password: this.password,
        email: this.email,
        phone: this.phone,
        confirmPassword: this.confirmPassword,
        role: this.role
      };

      try {
        // Отправляем данные на сервер
        const response = await axios.post('http://app-backend:8000/api/auth/register', dataToSend, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log('Data sent successfully:', response.data);
      } catch (error) {
        console.error('Error sending data:', error);
      }
    },
    async sendDataAuthorisation() {
      // Формируем JSON-объект
      const dataToSend = {
        login: this.login,
        password: this.password,
      };
      // Отправляем данные на сервер
      axios.post('http://app-backend:8000/api/auth/login', dataToSend, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(res => {
        console.log(res);
      })
          .catch(function (error) {
            console.log(error);
          });
    }
  }
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
</style>