<template>
    <form @submit.prevent="startSimulation">
      <div class="file-upload">
        <label for="fileUpload">Upload Excel Files:</label>
        <input type="file" id="fileUpload" @change="handleFileUpload" multiple accept=".xlsx, .xls" />
      </div>
      <button type="submit" class="submit-button">Start Simulation</button>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        files: []
      };
    },
    methods: {
      handleFileUpload(event) {
        this.files = Array.from(event.target.files);
        console.log("Files uploaded:", this.files);
      },
      startSimulation() {
        console.log("Files:", this.files);
        // handle excel files here
      }
    }
  };
  </script>
  