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
export default {
  data() {
    return {
      settingsFile: [],
      attributesFile: [],
      connectionsFile: []
    };
  },
  methods: {
    startSimulation() {
      console.log("Files:", this.files);
      // handle excel files here
    },


    handleSettingsUpload(event) {
      this.settingsFiles = Array.from(event.target.files);
      console.log("Settings uploaded: ", this.settingsFiles);

      // Create FormData object and append the settings file to ti
      const formData = new FormData();
      formData.append('settings', this.settingsFile[0]);

      // TO DO ---> Send axios.post to backend/Flask
    },

    
    handleAttributesUpload(event) {
      this.attributesFile = Array.from(event.target.files);
      console.log("Attributes uploaded: ", this.attributesFiles);
    },
    handleConnectionsUpload(event) {
      this.connectionsFile = Array.from(event.target.files);
      console.log("Connections uploaded: ", this.connectionsFile);
    }
  }
};
</script>