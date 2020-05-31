import Vue from 'vue'
import Router from 'vue-router'


const login = r => require.ensure([], () => r(require('../components/login.vue')), 'login')

const index = r => require.ensure([], () => r(require('../components/index.vue')), 'index')


Vue.use(Router)
var router = new Router({
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/index',
      component: index,
      name: 'index',
    }
  ]
})

export default router
