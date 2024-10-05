<template>
  <h2>Upload User File</h2>
  <form @submit.prevent="startSimulation" class="file-upload-form">
    <div class="file-upload-row">
      <label for="settingsUpload">Simulation Settings:</label>
      <input type="file" id="settingsUpload" class="custom-upload-btn-grey" @change="handleSettingsUpload" accept=".xlsx, .xls" />
    </div>

    <div class="file-upload-row">
      <label for="attributesUpload">Node Attributes:</label>
      <input type="file" id="attributesUpload" class="custom-upload-btn-grey" @change="handleAttributesUpload" accept=".xlsx, .xls" />
    </div>

    <div class="file-upload-row">
      <label for="connectionsUpload">Node Connections:</label>
      <input type="file" id="connectionsUpload" class="custom-upload-btn-grey" @change="handleConnectionsUpload" accept=".xlsx, .xls" />
    </div>
    
    <button type="submit" class="submit-button">Upload Files</button>
  </form>

  <div v-if="display_params">
    <router-link to="/gameplay">View Parameters</router-link>
  </div>
  
  <div v-if="errors" class="error-container">
    
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
      invalid_value: false
    };
  },
  methods: {
    async startSimulation() {
      const path = 'http://127.0.0.1:5000/excel_import';

      this.errors = null;
      this.invalid_value = false;

      try {
        const response = await axios.post(path, this.file_data);
        this.params = response.data;
        this.display_params = true;
        // Optional: Redirect after successful submission
        this.$router.push('/preview'); // Uncomment if you want to redirect to parameters view
      } catch (error) {
        this.show_errors = true;
        this.file_data.delete("settings_file");
        this.file_data.delete("attributes_fies");
        this.file_data.delete("connections_file");
        
        if (error.status == 500) {
          this.errors = error.response.data.error;
          return;
        }

        if (error.response) {
          this.errors = `Error occurred when importing files: ${error.response?.data?.error || error.message || error}`;
          console.log("Unable to upload/read files. Error: ", error);
          this.invalid_value = true;
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors,
            },
          });
        } else {
          console.log("Unable to upload/read files. Error: ", error);
          this.errors = `Error occurred when importing files: ${error}`;
          console.log(this.errors);
          alert("Unable to upload/read files.");
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors,
            },
          });
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
