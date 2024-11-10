
export default {
    state: {
        userName: '',
        lastname: '',
        middlename: ''
    },
    mutations: {
        SET_USER_DATA(state, payload) {
            state.userName = payload.name;
            state.lastname = payload.lastname;
            state.middlename = payload.middlename;
        }
    },
    actions: {
        setUserData({ commit }, userData) {
            commit('SET_USER_DATA', userData);
        }
    },
    getters: {
        fullName: (state) => `${state.userName} ${state.lastname} ${state.middlename}`
    }
};
