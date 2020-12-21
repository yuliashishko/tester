<template>
  <div>
    <Navigation></Navigation>
  <div class="container p-5">
    <div class="row">
      <div class="col-sm-10">
        <h1>People</h1>
        <hr>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.people-modal>Add User</button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Group</th>
            <th scope="col">Username</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(people, index) in people" :key="index">
            <td>{{ people.name }}</td>
            <td>{{ people.group }}</td>
            <td>{{ people.username }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.people-update-modal
                  @click="editPeople(people)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeletePeople(people)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addPeopleModal"
             id="people-modal"
             title="Add a new user"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                      label="name:"
                      label-for="form-nae-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addPeopleForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-group-group"
                      label="Group:"
                      label-for="form-group-input">
          <b-form-input id="form-group-input"
                        type="text"
                        v-model="addPeopleForm.group"
                        required
                        placeholder="Enter group">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-username-group"
                         label="Username:"
                         label-for="form-username-input">
          <b-form-input id="form-username-input"
                        type="text"
                        v-model="addPeopleForm.username"
                        required
                        placeholder="Enter username">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group"
                         label="Password:"
                         label-for="form-password-input">
          <b-form-input id="form-password-input"
                        type="text"
                        v-model="addPeopleForm.password"
                        required
                        placeholder="Enter password">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editPeopleModal"
             id="people-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-group-edit-group"
                      label="Group:"
                      label-for="form-group-edit-input">
          <b-form-input id="form-group-edit-input"
                        type="text"
                        v-model="editForm.group"
                        required
                        placeholder="Enter group">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-username-edit-group"
                      label="Username:"
                      label-for="form-username-edit-input">
          <b-form-input id="form-group-username-input"
                        type="text"
                        v-model="editForm.username"
                        required
                        placeholder="Enter username">
          </b-form-input>
          <b-form-group id="form-password-edit-group"
                        label="Password:"
                        label-for="form-password-edit-input">
            <b-form-input id="form-password-edit-input"
                          type="text"
                          v-model="editForm.password"
                          required
                          placeholder="Enter password">
            </b-form-input>
          </b-form-group>
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
import Navigation from "./Navigation";

export default {
  data() {
    return {
      people: [],
      addPeopleForm: {
        id_people: '',
        name: '',
        group: '',
        username: '',
        password: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id_people: '',
        name: '',
        group: '',
        username: '',
        password: '',
      },
    };
  },
  components: {
    Navigation,
    alert: Alert,
  },
  methods: {
    getPeople() {
      const path = 'http://localhost:5000/people';
      axios.get(path)
        .then((res) => {
          this.people = res.data.people;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPeople(payload) {
      const path = 'http://localhost:5000/people';
      axios.post(path, payload)
        .then(() => {
          this.getPeople();
          this.message = 'User added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getPeople();
        });
    },
    initForm() {
      this.addPeopleForm.name = '';
      this.addPeopleForm.group = '';
      this.addPeopleForm.username = [];
      this.addPeopleForm.password = [];
      this.editForm.id_people = '';
      this.editForm.name = '';
      this.editForm.group = '';
      this.editForm.username = '';
      this.editForm.password = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPeopleModal.hide();
      const payload = {
        name: this.addPeopleForm.name,
        group: this.addPeopleForm.group,
        username: this.addPeopleForm.username,
        password: this.addPeopleForm.password, // property shorthand
      };
      this.addPeople(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPeopleModal.hide();
      this.initForm();
    },
    editPeople(people) {
      this.editForm = people;
      this.editForm.password = '';
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPeopleModal.hide();
      const payload = {
        name: this.editForm.name,
        group: this.editForm.group,
        username: this.editForm.username,
        password: this.editForm.password,
      };
      this.updatePeople(payload, this.editForm.id_people);
    },
    updatePeople(payload, id_people) {
      const path = `http://localhost:5000/people/${id_people}`;
      axios.put(path, payload)
        .then(() => {
          this.getPeople();
          this.message = 'User updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPeople();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPeopleModal.hide();
      this.initForm();
      this.getPeople(); // why?
    },
    removePeople(id_people) {
      const path = `http://localhost:5000/people/${id_people}`;
      axios.delete(path)
        .then(() => {
          this.getPeople();
          this.message = 'User removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPeople();
        });
    },
    onDeletePeople(people) {
      this.removePeople(people.id_people);
    },
  },
  created() {
    this.getPeople();
  },
};
</script>
