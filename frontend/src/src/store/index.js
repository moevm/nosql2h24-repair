import { createStore } from 'vuex';

const store = createStore({
    state: {
        // Список пользователей
        user: JSON.parse(localStorage.getItem('user')) || []
    },
    mutations: {
        // Удаление всех пользователей
        removeUsers(state) {
            state.user = []; // Очистка массива пользователей
            localStorage.removeItem('user'); // Удаление из localStorage
        },
        // Добавление одного пользователя с очисткой старых данных
        addSingleUser(state, user) {
            state.user= [user]; // Заменяем массив только одним пользователем
            localStorage.setItem('user', JSON.stringify(state.user)); // Сохраняем в localStorage
        }
    },
    getters: {
        // Получение всех пользователей
        getUser(state) {
            return state.user;
        }
    }
});

export default store;
