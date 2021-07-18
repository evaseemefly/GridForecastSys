import Vue from 'vue'
import Router from 'vue-router'

import home from '../layout/home/index.vue'
// import login from '../layout/login/login.vue';
import content from '../layout/content/center_map.vue'
import gridcontent from '../layout/content/center_map_grid.vue'
import contentForecast from '../layout/content/center_map_forecast.vue'
// 引入浮标content
import fubcontent from '../layout/content/center_map_fub.vue'
// 引入风暴潮content
import stormcontent from '../layout/content/center_map_storm.vue'
// 路由改为组件的方式引入，不再使用require
// const routers = [
//   {
//     path: '/home',
//     name: 'home',
//     component: home,
//     children: [
//       // {
//       //   name: 'content',
//       //           // path:'content/:did',
//       //   // path: 'content/:code/:category',
//       //   path: 'content',
//       //   // component: content,
//       //   children: [
//       //     {
//       //       name: 'storm',
//       //       path: 'storm/:code',
//       //       component: content
//       //     },
//       //     {
//       //       name: 'grid',
//       //       path: 'grid/:code',
//       //       component: content
//       //     },
//       //     {
//       //       name: 'forecast',
//       //       path: 'forecast/:code',
//       //       component: contentForecast
//       //     }

//       //   ]

//       // },
//       {
//         name: 'storm',
//         path: 'content/storm/:code',
//         component: stormcontent
//       },
//       {
//         name: 'grid',
//         path: 'content/grid/:code',
//         component: gridcontent
//       },
//       {
//         name: 'forecast',
//         path: 'content/forecast/:code',
//         component: contentForecast
//       },
//       {
//         name: 'fub',
//         path: 'content/fub/:code',
//         component: fubcontent
//       }
//     ]
//   }
// ]

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      // 注意以/ 开头的嵌套路径会被当做根路径
      path: '/home',
      component: home,
      children: [
        {
          name: 'storm',
          path: 'content/storm/:code',
          component: stormcontent
        },
        {
          name: 'grid',
          path: 'content/grid/:code',
          component: gridcontent
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
  ]
})

// export default routers
