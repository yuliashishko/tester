<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Questions</h1>
        <hr>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.question-modal>Add question</button>
        <br><br>
        <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Question text</th>
                <th scope="col">Maximum mark</th>
                <th></th>
              </tr>
            </thead>
          <tbody>
          <tr v-for="(question, index) in questions" :key="index">
            <td>{{question.question_text }}</td>
            <td>{{question.max_mark }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.question-update-modal
                  @click="editQuestion(question)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteQuestion(question)">
                  Delete
                </button>
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  @click="showAnswers(question)">
                  Answers
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addQuestionModal"
             id="question-modal"
             title="Add a new question"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-text-group"
                      label="text:"
                      label-for="form-name-input">
          <b-form-input id="form-text-input"
                        type="text"
                        v-model="addQuestionForm.question_text"
                        required
                        placeholder="Enter question text">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-mark-group"
                      label="Maximum mark:"
                      label-for="form-mark-input">
          <b-form-input id="form-mark-input"
                        type="text"
                        v-model="addQuestionForm.max_mark"
                        required
                        placeholder="Enter maximum mark">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editQuestionModal"
             id="question-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-text-edit-group"
                      label="Question text:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-text-edit-input"
                        type="text"
                        v-model="editForm.question_text"
                        required
                        placeholder="Enter Question text">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-mark-edit-group"
                      label="Maximum mark:"
                      label-for="form-mark-edit-input">
          <b-form-input id="form-mark-edit-input"
                        type="text"
                        v-model="editForm.max_mark"
                        required
                        placeholder="Enter maximum mark">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";


export default {
  data() {
    return {
      questions: [],
      addQuestionForm: {
        id_question: '',
        max_mark: 0,
        question_text: '',
        answers: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id_question: '',
        max_mark: 0,
        question_text: '',
        answers: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getQuestions() {
      const path = 'http://localhost:5000/questions';
      axios.get(path)
        .then((res) => {
          this.questions = res.data.questions;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addQuestion(payload) {
      const path = 'http://localhost:5000/questions';
      axios.post(path, payload)
        .then(() => {
          this.getQuestions();
          this.message = 'Question added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getQuestions();
        });
    },
    initForm() {
      this.addQuestionForm.question_text = '';
      this.addQuestionForm.max_mark = 0;
      this.addQuestionForm.answers = [];
      this.editForm.id_question = '';
      this.editForm.question_text = '';
      this.editForm.max_mark = 0;
      this.editForm.answers = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addQuestionModal.hide();
      const payload = {
        max_mark: this.addQuestionForm.max_mark,
        question_text: this.addQuestionForm.question_text,
        answers: this.addQuestionForm.answers,
      };
      this.addQuestion(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addQuestionModal.hide();
      this.initForm();
    },
    editQuestion(question) {
      this.editForm = question;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editQuestionModal.hide();
      const payload = {
        question_text: this.editForm.question_text,
        max_mark: this.editForm.max_mark,
        answers: this.editForm.answers,
      };
      this.updateQuestion(payload, this.editForm.id_question);
    },
    updateQuestion(payload, id_question) {
      const path = `http://localhost:5000/questions/${id_question}`;
      axios.put(path, payload)
        .then(() => {
          this.getQuestions();
          this.message = 'Question updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getQuestions();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editQuestionModal.hide();
      this.initForm();
      this.getQuestions();
    },
    removeQuestion(id_question) {
      const path = `http://localhost:5000/questions/${id_question}`;
      axios.delete(path)
        .then(() => {
          this.getQuestions();
          this.message = 'Question removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getQuestions();
        });
    },
    onDeleteQuestion(question) {
      this.removeQuestion(question.id_question);
    },
    showAnswers(question) {
        Vue.$cookies.set('id_question', question.id_question)
        this.$router.push({name: 'Answers'})
    }
  },
  created() {
    this.getQuestions();
  },
};
</script>
