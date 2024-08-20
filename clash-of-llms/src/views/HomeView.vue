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

    <ParameterInputForm v-if="inputOption === 'manual'" />
    <FileUploadForm v-else />
  </div>
</template>

<script>
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
  }
};
</script>
