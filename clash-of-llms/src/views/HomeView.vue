<template>
  <div id="app" class="home">
    <!-- Always visible title -->
    <h1>Red vs Blue Team Simulation</h1>
    
    <!-- Option toggle for selecting input method -->
    <div class="option-toggle">
      <label>
        <input type="radio" v-model="inputOption" value="manual" />
        Enter Parameters
      </label>
      <label>
        <input type="radio" v-model="inputOption" value="upload" />
        Upload Excel Files
      </label>
    </div>

    <!-- Conditionally render the forms based on the selected option -->
    <ParameterInputForm v-if="inputOption === 'manual'" />
    <FileUploadForm v-else />
  </div>
</template>

<script>
import axios from 'axios';
import ParameterInputForm from '@/components/ParameterInput.vue';
import FileUploadForm from '@/components/FileUpload.vue';

export default {
  data() {
    return {
      inputOption: 'manual' // Default option
    };
  },
  components: {
    ParameterInputForm,
    FileUploadForm
  },
  methods: {
    downloadExcel() {
      axios({
        url: 'http://localhost:5000/excel_export', 
        method: 'GET',
        responseType: 'blob', 
      })
      .then((response) => {
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);

        const now = new Date();
        const timestamp = now.getHours() + "_" + now.getMinutes() + "_" + now.getSeconds();
        const excel_file_name = `clash_of_llms_${timestamp}.xlsx`;
        link.download = excel_file_name; 
        link.click();
        window.URL.revokeObjectURL(link.href);
      })
      .catch((error) => {
        console.error('Error downloading the Excel file:', error);
      });
    },
  },
};
</script>

<style scoped>
/* Add your styling here */
</style>
