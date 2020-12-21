<template>
  <div>
    <Navigation></Navigation>
    <div class="Container p-5">
      <b-form>
        <h1>Get new Exam</h1>
        <alert :message=message v-if="showMessage"></alert>
        <div class="form-group">
          <b-input type="text" name="name" v-model="test_name" placeholder="Test Name"/>
        </div>
        <b-button a @click="findTest(test_name)"> Find test</b-button>
        <br>
      </b-form>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";
import Navigation from "./Navigation";

export default {

  name: 'Main',
  data() {
    return {
      showMessage: false,
      test_name: '',
    }
  },

  components: {
    Navigation: Navigation,
    alert: Alert,
  },
  methods: {
    findTest(name) {
      const path = `http://localhost:5000/findtest/${name}`;
      axios.get(path)
        .then((res) => {
          if (res.data.status) {
            Vue.$cookies.set('test_name', name);
            this.$router.push({name: 'TestExam'});
          } else {
            this.message = res.data.message;
            this.showMessage = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    }
  },
  created() {
    this.logged = Vue.$cookies.get("token") != null;
  }
}
</script>

