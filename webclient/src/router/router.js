import Vue from 'vue'
import Router from 'vue-router'

import home from '../layout/home/index.vue'
// import login from '../layout/login/login.vue';
import content from '../layout/content/center_map.vue'
import contentForecast from '../layout/content/center_map_forecast.vue'
// 引入浮标content
import fubcontent from '../layout/content/center_map_fub.vue'

// 路由改为组件的方式引入，不再使用require
const routers = [
  {
    path: '/home',
    name: 'home',
    component: home,
    children: [
      // {
      //   name: 'content',
      //           // path:'content/:did',
      //   // path: 'content/:code/:category',
      //   path: 'content',
      //   // component: content,
      //   children: [
      //     {
      //       name: 'storm',
      //       path: 'storm/:code',
      //       component: content
      //     },
      //     {
      //       name: 'grid',
      //       path: 'grid/:code',
      //       component: content
      //     },
      //     {
      //       name: 'forecast',
      //       path: 'forecast/:code',
      //       component: contentForecast
      //     }

      //   ]

      // },
      {
        name: 'storm',
        path: 'content/storm/:code',
        component: content
      },
      {
        name: 'grid',
        path: 'content/grid/:code',
        component: content
      },
      {
        name: 'forecast',
        path: 'content/forecast/:code',
        component: contentForecast
      },
      {
        name: 'fub',
        path: 'content/fub/:code',
        component: fubcontent
      }
    ]
  }
  // {
  //     path:'/login',
  //     component:login
  // }
]
export default routers
