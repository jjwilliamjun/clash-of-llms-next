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

  <div v-if="blue_team">
    <p>{{ blue_team }}</p>
  </div>

  <div v-if="red_team">
    <p>{{ red_team }}</p>
  </div>

  <div v-if="node_attributes">
    <p>{{ node_attributes }}</p>
  </div>

  <div v-if="node_connections">
    <p>{{ node_connections }}</p>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      Files: [],
      file_data: new FormData, 
      params: null,
      blue_team: null,
      red_team: null, 
      node_attributes: null,
      node_connections: null
    };
  },
  methods: {
    async startSimulation() {
      // TO DO --> condition check 3 files uploaded

      const path = 'http://127.0.0.1:5000/excel_api/excel_import';

      try {
        const response = axios.post(path, this.file_data);
        this.params = (await response).data;

        // TO DO --> CHANGE TO USE DATA FROM CLASSES
        this.blue_team = this.params[1];
        this.red_team = this.params[0];
        this.node_attributes = this.params[2];
        this.node_connections = this.params[3];
        
      } catch (error) {
        // TO DO --> error handling
        console.log("didn't work", error);
      }
    },
    handleSettingsUpload() {
      const settings_file = document.getElementById("settingsUpload").files[0];
      console.log("Settings uploaded: ", settings_file);
      this.file_data.append('settings_file', settings_file);
    },
    handleAttributesUpload() {
      const attributes_file = document.getElementById("attributesUpload").files[0];
      console.log("Attributes uploaded: ", attributes_file);
      this.file_data.append('attributes_file', attributes_file)
    },
    handleConnectionsUpload() {
      const connections_file = document.getElementById("connectionsUpload").files[0];
      console.log("Settings uploaded: ", connections_file);
      this.file_data.append('connections_file', connections_file)
    }
  }
};
</script>