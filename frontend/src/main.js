import { createApp } from 'vue';
import App from './App.vue';
import router from './src/router';
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://172.18.0.4:8000/';  // the FastAPI backend
axios.defaults.headers = {
	'Access-Control-Allow-Origin' : '*',
	'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
	'Access-Control-Allow-Headers': '*'
}

const app = createApp(App); // Создание экземпляра приложения
app.use(router); // Использование маршрутизатора
app.mount('#app'); // Монтирование приложения в DOM