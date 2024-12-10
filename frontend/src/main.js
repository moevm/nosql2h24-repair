import { createApp } from 'vue';
import App from './App.vue';
import router from './src/router';
import axios from 'axios';
import store from './src/store';

axios.defaults.withCredentials = true;
if (window.location.hostname.startsWith('127.0.0.1')) {
	axios.defaults.baseURL = 'http://127.0.0.1:8000/';
}
if (window.location.hostname.startsWith('localhost')) {
	axios.defaults.baseURL = 'http://localhost:8000/';
}
axios.defaults.headers = {
	'Access-Control-Allow-Origin' : '*',
	'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
	'Access-Control-Allow-Headers': '*',
	'Content-Type': 'application/x-www-form-urlencoded'
}

const app = createApp(App); // Создание экземпляра приложения
app.use(router); // Использование маршрутизатора
app.use(store);
app.mount('#app'); // Монтирование приложения в DOM