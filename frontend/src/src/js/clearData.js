import { useStore } from 'vuex'; // Для работы с хранилищем Vuex
import { clearAllCookies } from './useCookies'; // Импорт функции очистки куков
import { useRouter } from 'vue-router'; // Доступ к роутеру

export const clearData = () => {
    const store = useStore(); // Доступ к хранилищу Vuex
    const router = useRouter();
    // Очистка всех куков
    clearAllCookies();

    // Очистка данных в Vuex
    store.commit('removeUsers');
    router.push('/login');
};