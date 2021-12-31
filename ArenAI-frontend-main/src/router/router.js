import { createRouter,createWebHistory} from "vue-router";

const routes = [
    {
        path: '/',
        redirect: '/gamecenter'
    },
    {
        path: "/login",
        name: "Login",
        component:  () => import('../views/login/Login.vue'),
    },
    {
        path: "/signup",
        name: "SignUp",
        component:  () => import('../views/login/SignUp.vue'),
    },
    {
        path: "/gamecenter",
        name: "Game Center",
        component: () => import('../views/frame/Frame.vue'),
        children: [
            {path: '', component: () => import('../views/game-center/CenterContent.vue') }
        ]
    },
    {
        path: "/games/:gameName",
        name: "Games",
        component: () => import ('../views/frame/Frame.vue'),
        children: [
            { path:'',  component: () => import('../views/game/Game.vue') }
        ]
        
        // children: [
        //     { path: 'battle', component: () => import('../components/games/battle/Battle.vue')},
        //     { path: 'gomoku', component: () => import('../components/games/Gomoku/Gomoku.vue')}
        // ]
    },
    {
        path: "/match/:gameName",
        name: 'match',
        component: () => import ('../views/frame/Frame.vue'),
        children : [
            { path: '', component: () => import('../components/games/Games.vue') }
        ]
    },
    {
        path: "/profile/:item?",
        component: () => import('../views/profile/Profile.vue')
    },
    {
        path: "/about",
        component: () => import ('../views/frame/Frame.vue'),
        children: [
            {path: '', component: () => import('../views/about/About.vue')}
        ]
    }
    // {
    //     path: "/test",
    //     name: "test",
    //     component:  () => import('../views/Test.vue'),
    // },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
