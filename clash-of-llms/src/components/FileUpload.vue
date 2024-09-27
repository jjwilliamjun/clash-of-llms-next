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
  
  <div v-if="show_errors" class="error-container">
    
    <span v-if="invalid_value">
      <strong>Error in Excel input:</strong>
      <div v-for="(value, key) in errors" :key="key" class="error-message">
        {{ value }}
      </div>
    </span>
    <span v-else>
      <strong>Error in Excel input: {{ errors }}</strong>
    </span>
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
      errors: null,
      invalid_value: false,
      show_errors: false
    };
  },
  methods: {
    async startSimulation() {
      const path = 'http://127.0.0.1:5000/excel_import';

      this.errors = null;
      this.invalid_value = false;
      this.show_errors = false;

      try {
        const response = await axios.post(path, this.file_data);
        this.params = response.data;
        this.display_params = true;
        // Optional: Redirect after successful submission
        this.$router.push('/preview'); // Uncomment if you want to redirect to parameters view
      } catch (error) {


        console.log("FILEDATA BEFORE: ", this.file_data);

        this.show_errors = true;
        this.file_data.delete("settings_file");
        this.file_data.delete("attributes_fies");
        this.file_data.delete("connections_file");

        console.log("FILEDATA AFTER: ", this.file_data);
        
        if (error.status == 500) {
          this.errors = error.response.data.error;
          return;
        }

        if (error.response) {
          this.errors = error.response.data.error;
          console.log("Unable to upload/read files. Error: ", error);
          this.invalid_value = true;
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
