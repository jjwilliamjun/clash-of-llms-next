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
    
    <button type="submit" class="submit-button">Start Simulation</button>
  </form>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      fileData: []
    };
  },
  methods: {
    startSimulation() {
      console.log("Files:", this.files);
      // handle excel files here
    },


    handleSettingsUpload() {
      const settingsFile = document.getElementById("settingsUpload").files[0];
      console.log("Settings uploaded: ", settingsFile);

      const path = 'http://127.0.0.1:5000/excel_api/excel_import'

      const formData = new FormData();
      formData.append('file', settingsFile);

      const response = axios.post(path, formData)
        .then(() => {
            console.log("worked!");
            console.log(response);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
    },
    
    handleAttributesUpload() {
      const attrFile = document.getElementById("attributesUpload").files[0];
      console.log("Attributes uploaded: ", attrFile);

      const path = 'http://127.0.0.1:5000/excel_api/excel_import'

      const formData = new FormData();
      formData.append('file', attrFile);

      const response = axios.post(path, formData)
        .then(() => {
            console.log("worked!");
            console.log(response);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
    },

    handleConnectionsUpload() {
      const connectionsFile = document.getElementById("connectionsUpload").files[0];
      console.log("Settings uploaded: ", connectionsFile);

      const path = 'http://127.0.0.1:5000/excel_api/excel_import'

      const formData = new FormData();
      formData.append('file', connectionsFile);

      const response = axios.post(path, formData)
        .then(() => {
            console.log("worked!");
            console.log(response);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
    }
  }
};
</script>