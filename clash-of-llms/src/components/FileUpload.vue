<template>

  <form @submit.prevent="startSimulation">
    <div class="file-upload">
      <label for="settingsUpload">Simulation Settings: </label>
      <input type="file" id="settingsUpload" @change="handleSettingsUpload" accept=".xlsx, .xls" />
      <br>
    </div>

    <div class="file-upload">
      <label for="attributesUpload">Node Attributes: </label>
      <input type="file" id="attributesUpload" @change="handleAttributesUpload" accept=".xlsx, .xls" />
      <br>
    </div>

    <div class="file-upload">
      <label for="connectionsUpload">Node Connections: </label>
      <input type="file" id="connectionsUpload" @change="handleConnectionsUpload" accept=".xlsx, .xls" />
      <br>
    </div>
    
    <button type="submit" class="submit-button">Upload Files</button>
    <br>
  </form>

  <div v-if="display_params">
    <router-link to="/parameters">View Parameters</router-link>
  </div>
  
  <div v-if="errors">
    <strong>error in excel input: </strong>
    <div v-for="(value, key) in errors" :key="key" class="error-message">
        {{ value }}
      </div>
  </div>


</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      Files: [],
      file_data: new FormData,
      display_params: false, 
      params: null,
      errors: null
    };
  },
  methods: {
    async startSimulation() {

      const path = 'http://127.0.0.1:5000/excel_api/excel_import';
      try {
        const response = axios.post(path, this.file_data);
        this.params = (await response).data;
        this.display_params = true;
        
      } catch (error) {
        if (error.response) {
          this.errors = error.response.data.error;
          console.log("Unable to upload/read files. Error: ", error);
        } else {
          console.log("Unable to upload/read files. Error: ", error);
          alert("Unable to upload/read files.");
        }
      }
    },
    handleSettingsUpload() {
      const settings_file = document.getElementById("settingsUpload").files[0];
      // console.log("Settings uploaded: ", settings_file);
      this.file_data.append('settings_file', settings_file);
    },
    handleAttributesUpload() {
      const attributes_file = document.getElementById("attributesUpload").files[0];
      // console.log("Attributes uploaded: ", attributes_file);
      this.file_data.append('attributes_file', attributes_file)
    },
    handleConnectionsUpload() {
      const connections_file = document.getElementById("connectionsUpload").files[0];
      // console.log("Settings uploaded: ", connections_file);
      this.file_data.append('connections_file', connections_file)
    }
  }
};
</script>