// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable */

import Vue from 'vue'
import App from './App'
import router from './router/index'
import store from './store/vuex/index'
import ElementUI from 'element-ui';
import "element-ui/lib/theme-chalk/index.css";
import systemUtil from './utils/systemUtil'
import authApi from './utils/authapi'

Vue.use(ElementUI);


Vue.config.productionTip = false
/* eslint-disable no-new */
var vueApp = new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
Vue.prototype.systemUtil = systemUtil
Vue.prototype.authApi = authApi

systemUtil.vueApp = vueApp;
