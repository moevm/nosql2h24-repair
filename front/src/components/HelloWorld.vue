<template>
  <div class="hello">
    <p class="register-link">Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
    <p class="register-link">Нет аккаунта? <router-link to="/login">Войти</router-link></p>
    <p class="register-link">Нет аккаунта? <router-link to="/auth">Регистрация первая</router-link></p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
