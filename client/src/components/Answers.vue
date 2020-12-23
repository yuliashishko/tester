<template>
  <div>
    <Navigation></Navigation>
    <div class="container p-5">
      <div class="row">
        <div class="col-sm-10">
          <h1>Answers</h1>
          <hr>
          <br><br>
          <alert :message=message v-if="showMessage"></alert>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.answer-modal>Add answer</button>
          <br><br>
          <table class="table table-hover">
            <thead>
            <tr>
              <th scope="col">Answer text</th>
              <th scope="col">mark</th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(answer, index) in answers" :key="index">
              <td>{{ answer.answer_text }}</td>
              <td>{{ answer.mark }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.answer-update-modal
                    @click="editAnswer(answer)">
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteAnswer(answer)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
      <b-modal ref="addAnswerModal"
               id="answer-modal"
               title="Add a new answer"
               hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-text-group"
                        label="text:"
                        label-for="form-name-input">
            <b-form-input id="form-text-input"
                          type="text"
                          v-model="addAnswerForm.answer_text"
                          required
                          placeholder="Enter answer text">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-mark-group"
                        label="mark:"
                        label-for="form-mark-input">
            <b-form-input id="form-mark-input"
                          type="text"
                          v-model="addAnswerForm.mark"
                          required
                          placeholder="Enter mark">
            </b-form-input>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
      <b-modal ref="editAnswerModal"
               id="answer-update-modal"
               title="Update"
               hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group id="form-text-edit-group"
                        label="answer text:"
                        label-for="form-name-edit-input">
            <b-form-input id="form-text-edit-input"
                          type="text"
                          v-model="editForm.answer_text"
                          required
                          placeholder="Enter answer text">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-mark-edit-group"
                        label="mark:"
                        label-for="form-mark-edit-input">
            <b-form-input id="form-mark-edit-input"
                          type="text"
                          v-model="editForm.mark"
                          required
                          placeholder="Enter mark">
            </b-form-input>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Update</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import Vue from "vue";
import Navigation from "./Navigation";


export default {
  data() {
    return {
      answers: [],
      addAnswerForm: {
        id_answer: '',
        mark: 0,
        answer_text: '',
        id_question: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id_answer: '',
        mark: 0,
        answer_text: '',
        id_question: '',
      },
    };
  },
  components: {
    Navigation,
    alert: Alert,
  },
  methods: {
    getAnswers() {
      const curr_question_id = Vue.$cookies.get('id_question');
      const path = `http://localhost:5000/answers/${curr_question_id}`;
      axios.get(path)
        .then((res) => {
          this.answers = res.data.answer;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addAnswer(payload) {
      const curr_question_id = Vue.$cookies.get('id_question');
      const path = `http://localhost:5000/answers/${curr_question_id}`;
      axios.post(path, payload)
        .then(() => {
          this.getAnswers();
          this.message = 'Answer added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAnswers();
        });
    },
    initForm() {
      this.addAnswerForm.answer_text = '';
      this.addAnswerForm.mark = 0;
      this.editForm.id_answer = '';
      this.editForm.mark = 0;
      this.editForm.answer_text = '';
      this.editForm.id_question = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAnswerModal.hide();
      const payload = {
        mark: this.addAnswerForm.mark,
        answer_text: this.addAnswerForm.answer_text,
        id_question: Vue.$cookies.get('id_question'),
      };
      this.addAnswer(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addAnswerModal.hide();
      this.initForm();
    },
    editAnswer(answer) {
      this.editForm = answer;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAnswerModal.hide();
      const payload = {
        mark: this.editForm.mark,
        answer_text: this.editForm.answer_text,
        id_question: Vue.$cookies.get('id_question'),
      };
      this.updateAnswer(payload, this.editForm.id_answer);
    },
    updateAnswer(payload, id_answer) {
      const path = `http://localhost:5000/answers/${id_answer}`;
      axios.put(path, payload)
        .then(() => {
          this.getAnswers();
          this.message = 'Answer updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getAnswers();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAnswerModal.hide();
      this.initForm();
      this.getAnswers();
    },
    removeAnswer(id_answer) {
      const path = `http://localhost:5000/answers/${id_answer}`;
      axios.delete(path)
        .then(() => {
          this.getAnswers();
          this.message = 'Answer removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getAnswers();
        });
    },
    onDeleteAnswer(answer) {
      this.removeAnswer(answer.id_answer);
    },
  },
  created() {
    this.getAnswers();
  },
};
</script>
