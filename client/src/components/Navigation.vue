<template>
  <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <a class="navbar-brand" href="#">Navigation</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse"
            aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a @click="onHome()" class="nav-link" >Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
          <a @click="onTests()" class="nav-link">Tests</a>
        </li>
        <lo class="nav-item">
          <a @click="onQuestions()" class="nav-link">Questions</a>
        </lo>
        <lo class="nav-item">
          <a @click="onStatictics()" class="nav-link">Statistics</a>
        </lo>
      </ul>
      <div class="form-inline mt-2 mt-md-0">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <b-dropdown v-if="logged !== false" :text="my_name()" class="m-md-2">
              <b-dropdown-item v-if="logged !== ''" a @click="onLogout()">Logout</b-dropdown-item>
              <b-dropdown-item v-if="logged === ''" a @click="onLogin()">Login</b-dropdown-item>
              <b-dropdown-item v-if="logged === ''" a @click="onRegister()">Register</b-dropdown-item>
            </b-dropdown>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";

export default {

  name: 'Navigation',
  data() {
    return {
      showMessage: false,
      logged: false,
      message: '',
      status: '',
    }
  },

  components: {
    alert: Alert,
  },
  methods: {
    onLogin() {
      this.$router.push({name: 'Login'});
    },
    onLogout() {
      Vue.$cookies.set('token', null);
      this.$router.push({name: 'Login'});
    },
    onRegister() {
      this.$router.push({name: 'Registration'});
    },
    my_name() {
      return this.logged === '' ? 'Guest' : this.logged;
    },
    onHome() {
      this.$router.push({name: 'Main'});
    },
    onTests() {
      this.$router.push({name: 'Tests'});
    },
    onQuestions() {
      this.$router.push({name: 'Questions'});
    },
    onStatistics() {
      this.$router.push({name: 'Statistics'});
    },
  },
  created() {
      const path = 'http://localhost:5000/am_i_logged';
      var self = this;
      axios.get(path, {
        headers: {"Authorization": `Bearer ${Vue.$cookies.get('token')}`}
      }).then((res) => {
         self.logged = res.data.name;
      }).catch((error) => {
        self.logged = '';
      });
  }
}
</script>

