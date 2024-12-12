import { createStore } from 'vuex';

const store = createStore({
    state: {
        // Список пользователей
        user: JSON.parse(localStorage.getItem('user')) || [],
        workers: JSON.parse(localStorage.getItem('worker')) || [],
        endDateProject: JSON.parse(localStorage.getItem('endDateProject')) || [],
        startDateProject: JSON.parse(localStorage.getItem('startDateProject')) || [],
        startDateStage: JSON.parse(localStorage.getItem('startDateStage')) || [],
        endDateStage: JSON.parse(localStorage.getItem('endDateStage')) || [],
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
        },
        addEndProject(state, endProject) {
            state.endDateProject = endProject;
            localStorage.setItem('endDateProject', JSON.stringify(endProject));
        },
        addStartProject(state, startProject) {
            state.startDateProject = startProject;
            localStorage.setItem('startDateProject', JSON.stringify(startProject));
        },
        addStartStage(state, stage) {
            state.startDateStage = stage;
            localStorage.setItem('startDateStage', JSON.stringify(stage));
        },
        addEndStage(state, endStage) {
            state.endDateStage = endStage;
            localStorage.setItem('endDateStage', JSON.stringify(endStage));
        },
    },
    getters: {
        // Получение всех пользователей
        getUser(state) {
            return state.user;
        },
        getWorkers(state) {
            return state.workers;
        },
        getStartDateProject(state) {
            return state.startDateProject;
        },
        getEndDateProject(state) {
            return state.endDateProject;
        },
        getStartDateStage(state) {
            return state.startDateStage;
        },
        getEndDateStage(state) {
            return state.endDateStage;
        },
    }
});

export default store;
