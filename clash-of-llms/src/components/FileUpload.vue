<template>
  <h2>Upload User File</h2>
  <form @submit.prevent="startSimulation" class="file-upload-form">
    <div class="file-upload-row">
      <label for="settingsUpload">Simulation Settings:</label>
      <input type="file" id="settingsUpload" @change="handleSettingsUpload" accept=".xlsx, .xls" />
    </div>

    <div class="file-upload-row">
      <label for="attributesUpload">Node Attributes:</label>
      <input type="file" id="attributesUpload" @change="handleAttributesUpload" accept=".xlsx, .xls" />
    </div>

    <div class="file-upload-row">
      <label for="connectionsUpload">Node Connections:</label>
      <input type="file" id="connectionsUpload" @change="handleConnectionsUpload" accept=".xlsx, .xls" />
    </div>
    
    <button type="submit" class="submit-button">Upload Files</button>
  </form>

  <div v-if="display_params">
    <router-link to="/gameplay">View Parameters</router-link>
  </div>
  
  <div v-if="errors" class="error-container">
    <strong>Error in Excel input:</strong>
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
      file_data: new FormData(),
      display_params: false, 
      params: null,
      errors: null
    };
  },
  methods: {
    async startSimulation() {
      const path = 'http://127.0.0.1:5000/excel_import';
      try {
        const response = await axios.post(path, this.file_data);
        this.params = response.data;
        this.display_params = true;
        // Optional: Redirect after successful submission
        this.$router.push('/preview'); // Uncomment if you want to redirect to parameters view
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
      this.file_data.append('settings_file', settings_file);
    },
    handleAttributesUpload() {
      const attributes_file = document.getElementById("attributesUpload").files[0];
      this.file_data.append('attributes_file', attributes_file);
    },
    handleConnectionsUpload() {
      const connections_file = document.getElementById("connectionsUpload").files[0];
      this.file_data.append('connections_file', connections_file);
    }
  }
};
</script>
