import Vue from 'vue';
import Router from 'vue-router';
import Books from './components/Books.vue';
import People from './components/People'
import Ping from './components/Ping.vue';
import Questions from "./components/Questions";
import VueCookies from 'vue-cookies'
Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/people',
      name: 'People',
      component: People,
    },
    {
      path: '/questions',
      name: 'Questions',
      component: Questions,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
