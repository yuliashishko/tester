import Vue from 'vue';
import Router from 'vue-router';
import Books from './components/Books.vue';
import People from './components/People'
import Ping from './components/Ping.vue';
import Questions from "./components/Questions";
import VueCookies from 'vue-cookies'
import Answers from "./components/Answers";
import Tests from "./components/Tests";
import Login from "./components/Login";
import Registration from "./components/Registration";
import Main from "./components/Main";
import TestExam from "./components/TestExam";
import Statistics from "./components/Statistics";

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
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
      path: '/',
      name: 'Main',
      component: Main,
    },
    {
      path: '/answers',
      name: 'Answers',
      component: Answers,
    },
    {
      path: '/findtest',
      name: 'TestExam',
      component: TestExam,
    },
    {
      path: '/tests',
      name: 'Tests',
      component: Tests,
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration,
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: Statistics,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
