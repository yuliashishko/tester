<template>
  <div>
    <Navigation></Navigation>

    <div class="Container p-5">
      <h1>Test</h1>

      <b-form v-for="(question, index) in questions" :key="index">
        <p>{{ question.question_text }}</p>
        <div class="input-group">
          <div class="custom-control custom-radio">
            <div class="input-group" v-for="(answer, ans_index) in answers[question.id_question]">
              <input
                type="radio"
                :id="answer.id_answer"
                :name="question.id_question"
                class="custom-control-input"
                :value="answer.id_answer"
                v-model="question.selected">
              <label class="custom-control-label" :for="answer.id_answer">{{ answer.answer_text }}</label>
            </div>
          </div>
        </div>

      </b-form>
      <b-button a @click="onFinish()">Finish</b-button>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";
import Navigation from "./Navigation";

export default {

  name: 'TestExam',
  data() {
    return {
      showMessage: false,
      logged: true,
      message: '',
      status: '',
      test_name: Vue.$cookies.get('test_name'),
      questions: [],
      selected: {},
      answers: {},
      abc: '',
    }
  },

  components: {
    Navigation,
    alert: Alert,
  },
  methods: {
    getAnswers(questions, id_question) {
      const path = `http://localhost:5000/answers/${id_question}`;
      var self = this;
      axios.get(path)
        .then((res) => {
          if (res.data.status) {
            self.questions = questions;
            Vue.set(self.answers, id_question, res.data.answer);
          } else {
            self.message = res.data.message;
            self.showMessage = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    getQuestions() {
      var name = this.test_name;
      const path = `http://localhost:5000/findtest/${name}`;
      var self = this;

      axios.get(path)
        .then((res) => {
          if (res.data.status === 'success') {
            for (var question of res.data.test.questions) {
              self.getAnswers(res.data.test.questions, question.id_question);
            }
          } else {
            self.message = res.data.message;
            self.showMessage = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onFinish() {
      const path = 'http://localhost:5000/exams';
      var answers = [];
      for (var question of this.questions) {
        answers.push(question.selected)
      }
      var payload = {
        'answers': answers,
        'test_name': this.test_name,
      }
      axios.post(path, payload, {
        headers: {"Authorization": `Bearer ${Vue.$cookies.get('token')}`}
      }).then((res) => {
         this.$router.push({name: 'Main'});
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },

  created() {
    this.test_name = Vue.$cookies.get('test_name')
    this.getQuestions();

  }
}
</script>

