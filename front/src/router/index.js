import { createMemoryHistory, createRouter } from 'vue-router'
import Register from '@/components/RegisterComponent.vue';
import Login from '@/components/LoginComponent.vue';
import HelloWorld from "@/components/HelloWorld.vue";
import Auth from "@/components/AuthComponent.vue"

const routes = [
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/',
        name: 'Home',
        component: HelloWorld
    },
    {
        path: '/auth',
        name: 'Auth',
        component: Auth
    }
];

const router = createRouter({
    history: createMemoryHistory(),
    routes
})
export default router;
