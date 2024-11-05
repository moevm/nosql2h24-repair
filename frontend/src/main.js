import { createApp } from 'vue';
import App from './App.vue';
import router from './src/router';

const app = createApp(App); // Создание экземпляра приложения
app.use(router); // Использование маршрутизатора
app.mount('#app'); // Монтирование приложения в DOM