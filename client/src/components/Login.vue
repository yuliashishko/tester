<template>
  <b-form id="login">
    <div class="container">
      <h1>Login</h1>
       <alert :message=message v-if="showMessage"></alert>
      <b-input type="text" name="username" v-model="inputForm.username" placeholder="Username"/>
      <br>
      <b-input type="password" name="password" v-model="inputForm.password" placeholder="Password"/>
      <br>
      <b-button type="button" v-on:click="login()">Login</b-button>

    </div>
  </b-form>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";

export default {
  showMessage: false,
  message:'',
  status:'',
  name: 'Login',
  data() {
    return {
      inputForm: {
        username: "",
        password: ""
      }
    }
  },

  components: {
    alert: Alert,
  },
  methods: {
    login() {
      if (this.inputForm.username && this.inputForm.password) {
        const payload = {
          username: this.inputForm.username,
          password: this.inputForm.password,
        };
       this.checkLogin(payload);
      }
    },
    checkLogin(payload) {
      const path = 'http://localhost:5000/login';
      axios.post(path, payload)
        .then((res) => {
          if (res.data.status === false) {
            this.message = res.data.message;
            this.showMessage = true;
            this.status = false;
            this.$router.push({name: 'Login'})
          } else {
            this.status = true;
            Vue.$cookies.set('token', res.data.token)
            this.$router.push({name: 'Tests'})
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },

  }
}
</script>
