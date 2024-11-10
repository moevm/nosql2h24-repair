import { createApp } from 'vue';
import App from './App.vue';
import router from './src/router';
import store from './src/store';
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';  // the FastAPI backend
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