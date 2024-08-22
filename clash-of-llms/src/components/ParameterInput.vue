<template>
    <form @submit.prevent="startSimulation">
      <div class="input-grid">
        <div class="input-group" v-for="(param, index) in parameters" :key="index">
          <label :for="'param' + index">{{ param.label }}</label>
          <input type="text" :id="'param' + index" v-model="param.value"/>
        </div>
      </div>
      <button type="submit" class="submit-button">Start Simulation</button>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        parameters: [
          { label: 'Parameter 1', value: '' },
          { label: 'Parameter 2', value: '' },
          { label: 'Parameter 3', value: '' },
          { label: 'Parameter 4', value: '' },
          { label: 'Parameter 5', value: '' },
          { label: 'Parameter 6', value: '' },
          { label: 'Parameter 7', value: '' },
          { label: 'Parameter 8', value: '' }
        ]
      };
    },
    methods: {
      startSimulation() {
        console.log("Parameters:", this.parameters);
      }
    }
  };
  </script>
  