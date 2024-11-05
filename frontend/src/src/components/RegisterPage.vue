<template>
  <AuthForm title="Регистрация" buttonText="Зарегистрироваться" :isLogin="false" />
</template>

<script>
import AuthForm from '../components/AuthForm.vue';

export default {
  name: 'RegisterPage',
  components: {
    AuthForm,
  },
};
</script>

<style scoped>
/* Дополнительные стили для страницы регистрации, если необходимо */
</style>