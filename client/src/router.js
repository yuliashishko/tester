import Vue from 'vue';
import Router from 'vue-router';
import Books from './components/Books.vue';
import People from './components/People'
import Ping from './components/Ping.vue';
import Questions from "./components/Questions";
import VueCookies from 'vue-cookies'
import Answers from "./components/Answers";
import Tests from "./components/Tests";
import LoginComponent from "./components/Login";
import Registration from "./components/Registration";
import SecureComponent from "./components/Secure";

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
      path: '/answers',
      name: 'Answers',
      component: Answers,
    },
    {
      path: '/tests',
      name: 'Tests',
      component: Tests,
    },
    {
      path: "/login",
      name: "login",
      component: LoginComponent
    },
    {
      path: "/secure",
      name: "secure",
      component: SecureComponent
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
