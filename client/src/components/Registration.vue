<template>
  <b-form id="registration">
    <div class="container">
      <h1>Registration</h1>
      <alert :message=message v-if="showMessage"></alert>
      <b-input type="text" name="name" v-model="inputForm.name" placeholder="Name"/>
      <br>
      <b-input type="text" name="group" v-model="inputForm.group" placeholder="Group"/>
      <br>
      <b-input type="text" name="username" v-model="inputForm.username" placeholder="Username"/>
      <br>
      <b-input type="password" name="password" v-model="inputForm.password" placeholder="Password"/>
      <br>
      <b-button type="button" v-on:click="register()">Register</b-button>

    </div>
  </b-form>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";

export default {
  data() {
    return {
      showMessage: false,
      message: '',
      status: '',
      inputForm: {
        name: "",
        group: "",
        username: "",
        password: ""
      }
    }
  },
  components: {
    alert: Alert,
  },
  methods: {
    register() {
      if (this.inputForm.username && this.inputForm.password && this.inputForm.name && this.inputForm.group) {
        const payload = {
          name: this.inputForm.name,
          group: this.inputForm.group,
          username: this.inputForm.username,
          password: this.inputForm.password,
        };
        this.checkRegister(payload);
      }
    },
    initForm() {
      this.showMessage = false;
      this.message = '';
    },
    checkRegister(payload) {
      const path = 'http://localhost:5000/registration';
      axios.post(path, payload)
        .then((res) => {
          if (res.data.status === false) {
            this.message = res.data.message;
            this.showMessage = true;
          } else {
            this.message = "Registration complete!";
            this.showMessage = true;
            this.$router.push({name: 'Login'})
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },

  },
  created() {
    this.initForm();
  },
}
</script>
