<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Patients</h1>
          <hr><br><br>
          <alert :message=message v-if="showMessage"></alert>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.patient-modal>Add Patient</button>
          <br><br>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Surname</th>
                <th scope="col">Area</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(patient, index) in patients" :key="index">
                <td>{{ patient.id }}</td>
                <td>{{ patient.name }}</td>
                <td>{{ patient.second_name }}</td>
                <td>{{ patient.area }}</td>
                <td>
                  <button
                        type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.patient-update-modal
                        @click="editPatient(patient)">
                    Update
                  </button>
                  <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeletePatient(patient)">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <b-modal ref="addPatientModal"
                id="patient-modal"
                title="Add a new patient"
                hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
            <b-form-input id="form-name-input"
                        type="text"
                        v-model="addPatientForm.name"
                        required
                        placeholder="Enter name">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-surname-group"
                    label="Surname:"
                    label-for="form-surname-input">
            <b-form-input id="form-surname-input"
                        type="text"
                        v-model="addPatientForm.sec_name"
                        required
                        placeholder="Enter surname">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-area-group"
                    label="Area:"
                    label-for="form-area-input">
            <b-form-input id="form-area-input"
                        type="number"
                        v-model="addPatientForm.area"
                        required
                        placeholder="Enter area">
            </b-form-input>
        </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
        </b-modal>
        <b-modal ref="editPatientModal"
                id="patient-update-modal"
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
            <b-form-group id="form-surname-edit-group"
                        label="Surname:"
                        label-for="form-surname-edit-input">
                <b-form-input id="form-surname-edit-input"
                            type="text"
                            v-model="editForm.surname"
                            required
                            placeholder="Enter surname">
                </b-form-input>
            </b-form-group>
            <b-form-group id="form-area-edit-group"
                        label="Area:"
                        label-for="form-area-edit-input">
                <b-form-input id="form-area-edit-input"
                            type="number"
                            v-model="editForm.area"
                            required
                            placeholder="Enter area">
                </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Update</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
        </b-form>
        </b-modal>
    </div>
  </template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      patients: [],
      addPatientForm: {
        name: '',
        sec_name: '',
        area: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        surname: '',
        area: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPatients() {
      const path = 'http://localhost:5000/show';
      axios.get(path)
        .then((res) => {
          this.patients = res.data.patients;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });
    },
    addPatient(payload) {
      const path = 'http://localhost:5000/show';
      axios.post(path, payload)
        .then(() => {
          this.getPatients();
          this.message = 'Patient added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getPatients();
        });
    },
    initForm() {
      this.addPatientForm.name = '';
      this.addPatientForm.sec_name = '';
      this.addPatientForm.area = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.surname = '';
      this.editForm.area = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPatientModal.hide();
      const payload = {
        name: this.addPatientForm.name,
        sec_name: this.addPatientForm.sec_name,
        area: this.addPatientForm.area, 
      };
      this.addPatient(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPatientModal.hide();
      this.initForm();
    },
    editPatient(patient) {
      this.editForm = patient;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPatientModal.hide();
      const payload = {
        name: this.editForm.name,
        sec_name: this.editForm.surname,
        area: this.editForm.area,
      };
      this.updatePatient(payload, this.editForm.id);
    },
    updatePatient(payload, patientID) {
        const path = `http://localhost:5000/show/${patientID}`;
        axios.put(path, payload)
            .then(() => {
              this.getPatients();
              this.message = 'Patient updated!';
              this.showMessage = true;
            })
            .catch((error) => {
              // eslint-отключение следующей строки
              console.error(error);
              this.getPatients();
            });
    },
    onResetUpdate(evt) {
        evt.preventDefault();
        this.$refs.editPatientModal.hide();
        this.initForm();
        this.getPatients();
    },
    removePatient(patientID) {
        const path = `http://localhost:5000/show/${patientID}`;
        axios.delete(path)
            .then(() => {
             this.getPatients();
             this.message = 'Patient removed!';
             this.showMessage = true;
            })
             .catch((error) => {
             // eslint-отключение следующей строки
             console.error(error);
             this.getPatients();
            });
    },
    onDeletePatient(patient) {
        this.removePatient(patient.id);
    },
  },
  created() {
    this.getPatients();
  },
};
</script>

