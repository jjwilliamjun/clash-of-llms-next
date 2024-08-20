<template>
  <div id="app" class="home">
    <h1>Red vs Blue Team Simulation</h1>
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
        <div>
          <button @click="downloadExcel">Download Excel</button>
        </div>
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
      inputOption: 'manual'
    };
  },
  components: {
    ParameterInputForm,
    FileUploadForm
  },
  methods: {
    startSimulation() {
      console.log("Parameters:", this.parameters);
    },
    downloadExcel() {
      axios({
        url: 'http://localhost:5000/excel_api/export_excel', 
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
