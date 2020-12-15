import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import VueCookies from 'vue-cookies';
Vue.use(VueCookies);

Vue.use(BootstrapVue);

Vue.config.productionTip = false;
Vue.$cookies.config('7d')

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
