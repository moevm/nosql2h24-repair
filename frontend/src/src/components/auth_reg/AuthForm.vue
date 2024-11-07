<template>
    <div class="auth-container">
      <div class="auth-box">
        <h2>{{ isRegister ? 'Регистрация' : 'Авторизация' }}</h2>
  
        <!-- Поле логина -->
        <input v-model="email" type="text" placeholder="Логин(email)" />
  
        <!-- Поле пароля -->
        <input v-model="password" type="password" placeholder="Пароль" />
  
        <!-- Дополнительные поля для регистрации -->
        <template v-if="isRegister">
          <input v-model="name" type="email" placeholder="Имя" />
          <input v-model="lastname" type="tel" placeholder="Фамилия" />
          <input v-model="middlename" type="tel" placeholder="Отчество" />
          <input v-model="confirmPassword" type="password" placeholder="Повторите пароль" />
          <select v-model="role">
            <option value="" disabled>Выберите роль</option>
            <option value="Рабочий">Рабочий</option>
            <option value="Заказчик">Заказчик</option>
            <option value="Прораб">Прораб</option>
            <option value="Администратор">Администратор</option>
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
  // import { sendDataRegistration }from '@/src/js/auth_registr'
  import axios from 'axios'
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
        isRegister: false, // Определяет, находимся ли мы на странице регистрации или авторизации
      };
    },
    methods: {

      toggleRegister() {
        this.isRegister = !this.isRegister;
      },
      async authenticate() {

      },
        // Логика авторизации
  
        // axios.post('http://172.18.0.4:8000/api/auth/login',
        //     { email: "example@example.com", password: "password123" },
        //     {     headers: {
        //         'Content-Type': 'application/json',
        //         'Accept': 'application/json'
        //       },
        //       withCredentials: true
        //     }
        // )
        //     .then(res => {
        //       console.log(res);
        //     })
            // .catch(error => {
            //   console.error("Ошибка сети:", error.message);
            //   if (error.response) {
            //     console.error("Данные ответа:", error.response.data);
            //   } else if (error.request) {
            //     console.error("Запрос:", error.request);
            //   } else {
            //     console.error("Сообщение об ошибке:", error.message);
            //   }
            // })
        //     .catch(function (error) {
        //       console.log(error.toJSON());
        //     });
        // console.log("authenticate что-то получила");
        // // if (this.login === 'user' && this.password === 'password') {
        //   // Успешная авторизация
        //   this.$router.push('/main'); // Переход на основную страницу
        // } else {
        //   alert('Неверный логин или пароль');
        // }
      async register() {
        const dataToSend = {
          email: this.email,
          name: this.name,
          lastname: this.lastname,
          middlename: this.middlename,
          password: this.password,
          role: this.role
        }

        axios.post('http://172.18.0.4:8000/api/auth/register', dataToSend,
            {     headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              withCredentials: true
            }
        )
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
        })
      },
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
