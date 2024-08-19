<template>
  <div id="app" class="home">
    <h1>Red vs Blue Team Simulation</h1>
    <form @submit.prevent="startSimulation">
      <div class="input-grid">
        <div class="input-group" v-for="(param, index) in parameters" :key="index">
          <label :for="'param' + index">{{ param.label }}</label>
          <input type="text" :id="'param' + index" v-model="param.value" placeholder="Enter {{ param.label }}" />
        </div>
      </div>
      <button type="submit" class="submit-button">Start Simulation</button>
    </form>
  </div>
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

<style scoped>
.home {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.input-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 15px;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

label {
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 6px;
  box-sizing: border-box;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>
