import Vue from 'vue';
import Router,{RouteConfig} from 'vue-router';

import home from '../layout/home/index.vue';
// import login from '../layout/login/login.vue';
// import content from '../layout/home/content-main.vue'

// 路由改为组件的方式引入，不再使用require
const routers:RouteConfig[]=[
    {
        path:'/home',
        name:'home',
        component:home,
        // children:[
        //     {
        //         name:'content',
        //         // path:'content/:did',
        //         path:'content/:did',
        //         component:content
        //     }
        // ]
    },
    // {
    //     path:'/login',
    //     component:login        
    // }    
];

const router:Router=new Router({
    mode:'history',
    routes:routers
})

// export default routers;
export default router;