<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Tests</h1>
        <hr>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.test-modal>Add test</button>
        <br><br>
        <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Test name</th>
                <th scope="col">Maximum mark</th>
                <th scope="col">Duration</th>
                <th></th>
              </tr>
            </thead>
          <tbody>
          <tr v-for="(test, index) in tests" :key="index">
            <td>{{test.test_name }}</td>
            <td>{{test.max_mark }}</td>
            <td>{{test.duration }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.test-update-modal
                  @click="editTest(test)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteTest(test)">
                  Delete
                </button>
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  @click="editQuestions(test)">
                  Questions
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTestModal"
             id="test-modal"
             title="Add a new test"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                      label="name:"
                      label-for="form-name-input">
          <b-form-input id="form-text-input"
                        type="text"
                        v-model="addTestForm.test_name"
                        required
                        placeholder="Enter test name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-mark-group"
                      label="Maximum mark:"
                      label-for="form-mark-input">
          <b-form-input id="form-mark-input"
                        type="text"
                        v-model="addTestForm.max_mark"
                        required
                        placeholder="Enter maximum mark">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-duration-group"
                      label="Duration:"
                      label-for="form-duration-input">
          <b-form-input id="form-duration-input"
                        type="text"
                        v-model="addTestForm.duration"
                        required
                        placeholder="Enter Duration">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editTestModal"
             id="test-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Test name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.test_name"
                        required
                        placeholder="Enter test name">
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
        <b-form-group id="form-duration-edit-group"
                      label="Duration:"
                      label-for="form-duration-edit-input">
          <b-form-input id="form-duration-edit-input"
                        type="text"
                        v-model="editForm.duration"
                        required
                        placeholder="Enter duration">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="editQuestionsTestModal"
             id="test-questions-update-modal"
             title="Questions"
             hide-footer>
      <b-form @submit="onSubmitUpdateQuestions" @reset="onResetUpdateQuestions" class="w-100">

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



export default {
  data() {
    return {
      tests: [],
      addTestForm: {
        max_mark: 0,
        duration: 0,
        test_name: '',
        questions: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id_test: '',
        max_mark: 0,
        duration: 0,
        test_name: '',
        questions: [],
      },
      editQuestionsForm: {
        questions: [],
        another_questions: [],
      }
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getTests() {
      const path = 'http://localhost:5000/tests';
      axios.get(path)
        .then((res) => {
          this.tests = res.data.tests;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editQuestions(test) {
      const path = `http://localhost:5000/tests/${test.id_test}`;
      axios.get(path)
        .then((res) => {
          this.editQuestionsForm.questions = res.data.questions;
          this.editQuestionsForm.another_questions = res.data.another_questions;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addTest(payload) {
      const path = 'http://localhost:5000/tests';
      axios.post(path, payload)
        .then(() => {
          this.getTests();
          this.message = 'Test added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTests();
        });
    },
    initForm() {
      this.addTestForm.max_mark = 0;
      this.addTestForm.duration = 0;
      this.addTestForm.test_name = '';
      this.addTestForm.questions = [];
      this.editForm.id_test = '';
      this.editForm.max_mark = 0;
      this.editForm.duration = 0;
      this.editForm.test_name = '';
      this.editForm.questions = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTestModal.hide();
      const payload = {
        max_mark: this.addTestForm.max_mark,
        duration: this.addTestForm.duration,
        test_name: this.addTestForm.test_name,
      };
      this.addTest(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTestModal.hide();
      this.initForm();
    },
    onResetUpdateQuestions(evt) {
      evt.preventDefault();
      this.$refs.editQuestionsTestModal.hide();
      this.initForm();
    },
    editTest(test) {
      this.editForm = test;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTestModal.hide();
      const payload = {
        max_mark: this.editForm.max_mark,
        duration: this.editForm.duration,
        test_name: this.editForm.test_name,
      };
      this.updateTest(payload, this.editForm.id_test);
    },
    onSubmitUpdateQuestions(evt) {

    },
    updateTest(payload, id_test) {
      const path = `http://localhost:5000/tests/${id_test}`;
      axios.put(path, payload)
        .then(() => {
          this.getTests();
          this.message = 'Test updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getTests();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTestModal.hide();
      this.initForm();
      this.getTests();
    },
    removeTest(id_test) {
      const path = `http://localhost:5000/tests/${id_test}`;
      axios.delete(path)
        .then(() => {
          this.getTests();
          this.message = 'Test removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getTests();
        });
    },
    onDeleteTest(test) {
      this.removeTest(test.id_test);
    },
  },
  created() {
    this.getTests();
  },
};
</script>
