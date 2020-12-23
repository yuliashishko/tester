<template>
  <div>
    <Navigation></Navigation>
    <div class="Container p-5">
      <b-form>
        <h1>Get statistics about Exam</h1>
        <alert :message=message v-if="showMessage"></alert>
        <div class="form-group">
          <b-input type="text" name="name" v-model="test_name" placeholder="Test Name"/>
        </div>
        <b-select v-model="selected_groups" multiple class="form-control">
          <label>Example multiple select</label>
          <option v-for="(group, index) in groups">
            {{ group }}
          </option>

        </b-select>
        <b-button a @click="getStatistics(test_name, selected_groups)"> Get statistic</b-button>
        <br>
      </b-form>

      <table class="table table-hover">
        <thead>
        <tr>
          <th scope="col">Test Name</th>
          <th scope="col">Name</th>
          <th scope="col">Group</th>
          <th scope="col">Result</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(exam, index) in exams" :key="index">
          <td>{{ exam.test.test_name }}</td>
          <td>{{ exam.people.name }}</td>
          <td>{{ exam.people.group }}</td>
          <td>{{ exam.mark }}/{{ exam.test.max_mark }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";
import Navigation from "./Navigation";

export default {

  name: 'Statistics',
  data() {
    return {
      showMessage: false,
      test_name: '',
      groups: [1, 2, 3, 4, 5],
      selected_groups: [],
      exams: [],
    }
  },

  components: {
    Navigation: Navigation,
    alert: Alert,
  },
  methods: {
    getStatistics(name, groups) {
      const path = `http://localhost:5000/statistics`;
      var payload = {
        'groups': this.groups,
        'test_name': this.test_name,
      };
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${Vue.$cookies.get('token')}`}
      })
        .then((res) => {
          if (res.data.status === 'success') {
            this.exams = res.data.exams;

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

