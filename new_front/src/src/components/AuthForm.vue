<template>
    <div class="auth-form-container">
      <div class="auth-form">
        <h2 class="form-title">{{ isLogin ? 'Авторизация' : 'Регистрация' }}</h2>
        
        <form @submit.prevent="handleSubmit">
          <div class="form-field" v-if="isLogin">
            <input type="text" v-model="login" placeholder="Логин" required />
          </div>
          <div class="form-field" v-if="isLogin">
            <input type="password" v-model="password" placeholder="Пароль" required />
          </div>
  
          <div class="form-field" v-if="!isLogin">
            <input type="text" v-model="login" placeholder="Логин" required />
          </div>
          <div class="form-field" v-if="!isLogin">
            <input type="password" v-model="password" placeholder="Пароль" required />
          </div>
          <div class="form-field" v-if="!isLogin">
            <input type="email" v-model="email" placeholder="Email" required />
          </div>
          <div class="form-field" v-if="!isLogin">
            <input type="tel" v-model="phone" placeholder="Телефон" required />
          </div>
          <div class="form-field" v-if="!isLogin">
            <input type="password" v-model="confirmPassword" placeholder="Повторите пароль" required />
          </div>
          <div class="form-field" v-if="!isLogin">
            <select v-model="role" required>
              <option value="" disabled selected>Выберите роль</option>
              <option value="worker">Рабочий</option>
              <option value="customer">Заказчик</option>
              <option value="foreman">Прораб</option>
              <option value="admin">Админ</option>
            </select>
          </div>
  
          <button type="submit" class="auth-button">{{ isLogin ? 'Войти' : 'Зарегистрироваться' }}</button>
        </form>
  
        <div class="register-prompt">
          <span v-if="isLogin">Нет аккаунта? <a href="#" @click="toggleForm">Зарегистрируйся</a></span>
          <span v-else>Есть аккаунт? <a href="#" @click="toggleForm">Войти</a></span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isLogin: true,
        login: '',
        password: '',
        email: '',
        phone: '',
        confirmPassword: '',
        role: ''
      };
    },
    methods: {
      handleSubmit() {
        if (this.isLogin) {
          // Логика авторизации
          console.log('Авторизация:', this.login, this.password);
        } else {
          // Логика регистрации
          console.log('Регистрация:', this.login, this.password, this.email, this.phone, this.role);
        }
      },
      toggleForm() {
        this.isLogin = !this.isLogin;
      }
    }
  };
  </script>
  
  <style scoped>
  .auth-form-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .auth-form {
    position: relative;
    width: 480px;
    height: auto; /* Убираем фиксированную высоту для адаптивности */
    background: #ebebeb;
    border-radius: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .form-title {
    margin-bottom: 20px;
  }
  
  .form-field {
    position: relative;
    width: 380px;
    margin-bottom: 16px;
  }
  
  .form-field input,
  .form-field select {
    width: 100%;
    height: 36px; /* Общее значение высоты для всех полей */
    box-sizing: border-box;
    background: #fcfcfc;
    border: 1px solid #3f3f3f;
    border-radius: 13px;
    padding: 0 10px;
    font-size: 16px;
  }
  
  .auth-button {
    position: relative;
    width: 380px;
    height: 49px;
    background: #625b71;
    border-radius: 10px;
    border: none;
    color: #ffffff;
    font-family: 'Single Day', sans-serif; /* Замените на соответствующий шрифт */
    font-size: 16px;
    cursor: pointer;
    margin-bottom: 20px; /* Добавляем отступ снизу */
  }
  
  .register-prompt {
    position: relative; /* Изменяем на relative */
    width: 100%; /* Замените на 100% для центрирования */
    height: 30px;
    font-family: 'Single Day', sans-serif; /* Замените на соответствующий шрифт */
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 24px; /* 150% */
    display: flex;
    justify-content: center; /* Центрируем по горизонтали */
    align-items: center; /* Вертикальное выравнивание */
    color: #000000;
  }
  </style>
  