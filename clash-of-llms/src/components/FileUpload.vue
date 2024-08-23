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
      Files: [],
      settings_data: new FormData(),
      attributes_data: new FormData(),
      connections_data: new FormData(),
    };
  },
  methods: {
    startSimulation() {
      // TO DO --> condition check 3 files uploaded

      const path = 'http://127.0.0.1:5000/excel_api/excel_import'

      const response1 = axios.post(path, this.settings_data)
        .then(() => {
            console.log("worked!");
            console.log(response1);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
      
      const response2 = axios.post(path, this.attributes_data)
        .then(() => {
            console.log("worked!");
            console.log(response2);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
      
      const response3 = axios.post(path, this.connections_data)
        .then(() => {
            console.log("worked!");
            console.log(response3);
          })
          .catch((error) => {
            console.log("didn't work", error);
          });
    },
    handleSettingsUpload() {
      const settingsFile = document.getElementById("settingsUpload").files[0];
      console.log("Settings uploaded: ", settingsFile);
      this.settings_data.append('file', settingsFile);
    },
    handleAttributesUpload() {
      const attributes_file = document.getElementById("attributesUpload").files[0];
      console.log("Attributes uploaded: ", attributes_file);
      this.attributes_data.append('file', attributes_file)
    },
    handleConnectionsUpload() {
      const connections_file = document.getElementById("connectionsUpload").files[0];
      console.log("Settings uploaded: ", connections_file);
      this.connections_data.append('file', connections_file)
    }
  }
};
</script>