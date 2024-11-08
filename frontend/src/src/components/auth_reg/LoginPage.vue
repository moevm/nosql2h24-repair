<template>
  <AuthForm title="Авторизация" buttonText="Войти" :isLogin="true" />
</template>

<script>
import AuthForm from '../auth_reg/AuthForm.vue';

export default {
  name: 'LoginPage',
  components: {
    AuthForm,
  },
};
</script>

<style scoped>
/* Дополнительные стили для страницы логина, если необходимо */
</style>