<template>
    <!-- <form @submit.prevent="startSimulation">
      <div class="input-grid">
        <div class="input-group" v-for="(param, index) in parameters" :key="index">
          <label :for="'param' + index">{{ param.label }}</label>
          <input type="text" :id="'param' + index" v-model="param.value"/>
        </div>
      </div>
      <button type="submit" class="submit-button">Start Simulation</button>
    </form> -->
    <form @submit.prevent="startSimulation">
    <div class="flex-container">

      <div class="flex-child">
        <h2 id="blueTeam">Blue Team</h2>

        <div id="blueParameters">

          <div class="select-parameter">
            <label for="blue_model">Model: </label>
            <select name="blue_model" v-model="blue_team.Model_ID">
              <option v-for="(item, index) in models" :key="index" :value="item">{{ item }}</option>
            </select>
          </div>

          <div class="select-parameter">
            <label for="blue_energy">Energy: {{ blue_team.Energy }}</label>
            <br>
            <input type="range" id="blue_energy" max="100" value="50" step="1" v-model="blue_team.Energy">
          </div>

          <div class="select-parameter">
            <label for="blue_msgs">Number of Messages Generated per Turn: {{ blue_team.Msgs_Generated }}</label>
            <br>
            <input type="range" id="blue_msgs" max="10" value="5" step="1" v-model="blue_team.Msgs_Generated">
          </div>

          <div class="select-parameter">
            <label for="blue_temp">Temperature: {{ blue_team.Temperature }}</label>
            <br>
            <input type="range" id="blue_temp" min="0" max="1" value="0.5" step="0.01" v-model="blue_team.Temperature">
          </div>

          <div class="select-parameter">
            <label for="blue_factor">Influence Factor: {{ blue_team.Influence_Factor }}</label>
            <br>
            <input type="range" id="blue_factor" min="0" max="1" value="0.5" step="0.01" v-model="blue_team.Influence_Factor">
          </div>

        </div>
      </div>

      <div class="flex-child">
        <h2 id="redTeam">Red Team</h2>

        <div id="redParameters">
          <div class="select-parameter">
            <label for="red_model">Model: </label>
            <select name="red_model" id="model" v-model="red_team.Model_ID"> 
              <option v-for="(item, index) in models" :key="index" :value="item">{{ item }}</option>
            </select>
          </div>

          <div class="select-parameter">
            <label for="red_msgs">Number of Messages Generated per Turn: {{ red_team.Msgs_Generated }}</label>
            <br>
            <input type="range" id="red_msgs" class="accent" min="1" max="10" value="5" step="1" v-model="red_team.Msgs_Generated">
          </div>

          <div class="select-parameter">
            <label for="red_temp">Temperature: {{ red_team.Temperature }}</label>
            <br>
            <input type="range" id="red_temp" class="accent" min="0" max="1" value="0.5" step="0.01" v-model="red_team.Temperature">
          </div>

          <div class="select-parameter">
            <label for="red_factor">Influence Factor: {{ red_team.Influence_Factor }}</label>
            <br>
            <input type="range" id="red_factor" class="accent" min="0" max="1" value="0.5" step="0.01" v-model="red_team.Influence_Factor">
          </div>

        </div>
      </div>
    </div>
    <button type="submit" class="submit-button">Start Simulation</button>
  </form>

  <div v-if="display_params">
    <router-link to="/parameters">View Parameters</router-link>
  </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        models: ['gpt 3.5 turbo', 'custom'],
        parameters: [
          { label: 'Parameter 1', value: '' },
          { label: 'Parameter 2', value: '' },
          { label: 'Parameter 3', value: '' },
          { label: 'Parameter 4', value: '' },
          { label: 'Parameter 5', value: '' },
          { label: 'Parameter 6', value: '' },
          { label: 'Parameter 7', value: '' },
          { label: 'Parameter 8', value: '' }
        ],
        blue_team: {
          Team: 'Blue',
          Model_ID: 'gpt 3.5 turbo',
          Energy: 50,
          Msgs_Generated: 5,
          Temperature: 0.5,
          Influence_Factor: 0.5
        },
        red_team: {
          Team: 'Red',
          Model_ID: 'gpt 3.5 turbo',
          Energy: 50,
          Msgs_Generated: 5,
          Temperature: 0.5,
          Influence_Factor: 0.5
        },
        display_params: false
      };
    },
    methods: {
      async startSimulation() {
        let input = [this.red_team, this.blue_team];

        const path = 'http://127.0.0.1:5000/excel_api/ui_parameters';
        try {
          const response = axios.post(path, input);
          this.params = (await response).data;

          this.display_params = true;
          
        } catch (error) {
          // TO DO --> error handling
          console.log("Error: ", error);
        }
      }
    }
  };
  </script>
  