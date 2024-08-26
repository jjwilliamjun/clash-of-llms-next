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
    <br>
  </form>

  <div v-if="display_params">
    <div class="flex-container" v-if="display_params">
      <div class="flex-child">
        <div v-if="blue_team" color="blue">
          <p id="blueTeam">Team: {{ blue_team.Team }}</p>
          <p>Model: {{ blue_team.Model_ID }}</p>
          <p>Initial Energy Level: {{ blue_team.Initial_Energy_Level }}</p>
          <p>Number of Messages Generated Per Turn: {{ blue_team.Msgs_Generated }}</p>
          <p>Temperature: {{ blue_team.Temperature }}</p>
        </div>
      </div>

      <div class="flex-child">
        <div v-if="red_team">
          <p id="redTeam">Team: {{ red_team.Team }}</p>
          <p>Model: {{ red_team.Model_ID }}</p>
          <p>Number of Messages Generated Per Turn: {{ red_team.Msgs_Generated }}</p>
          <p>Temperature: {{ red_team.Temperature }}</p>
        </div>
      </div>
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
      blue_team: null,
      red_team: null, 
      node_attributes: null,
      node_connections: null
    };
  },
  methods: {
    async startSimulation() {

      const path = 'http://127.0.0.1:5000/excel_api/excel_import';

      // Send files to backend flask app
      try {
        const response = axios.post(path, this.file_data);
        this.params = (await response).data;

        if (this.params.length != 4) {
          alert("Requires exactly 3 files.");
          return;
        }

        // TO DO --> CHANGE TO USE DATA FROM CLASSES
        this.display_params = true;
        this.blue_team = this.params[1];
        this.red_team = this.params[0];
        this.node_attributes = this.params[2];
        this.node_connections = this.params[3];

        // TO DO --> Display node parameters
        
      } catch (error) {
        // TO DO --> error handling
        console.log("Unable to upload/read files. Error: ", error);
        alert("Unable to upload/read files.");
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