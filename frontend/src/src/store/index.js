import { createStore } from 'vuex';

const store = createStore({
    state: {
        // Список пользователей
        user: JSON.parse(localStorage.getItem('user')) || [],
        workers: JSON.parse(localStorage.getItem('worker')) || []
    },
    mutations: {
        // Удаление всех пользователей
        removeUsers(state) {
            state.user = []; // Очистка массива пользователей
            localStorage.removeItem('user'); // Удаление из localStorage
        },
        removeWorkers(state) {
            state.workers = []; // Очистка массива пользователей
            localStorage.removeItem('worker'); // Удаление из localStorage
        },
        // Добавление одного пользователя с очисткой старых данных
        addSingleUser(state, user) {
            state.user= [user]; // Заменяем массив только одним пользователем
            localStorage.setItem('user', JSON.stringify(state.user)); // Сохраняем в localStorage
        },
        addSingleWorker(state, worker) {
            state.workers.push(worker); // Заменяем массив только одним пользователем
            localStorage.setItem('worker', JSON.stringify(state.workers)); // Сохраняем в localStorage
        }
    },
    getters: {
        // Получение всех пользователей
        getUser(state) {
            return state.user;
        },
        getWorkers(state) {
            return state.workers;
        }
    }
});

export default store;
