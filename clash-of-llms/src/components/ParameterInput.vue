<template>
  <div>
    <!-- Form -->
    <form @submit.prevent="handleFormSubmit">
      <div class="flex-container">
        <!-- Blue Team Settings -->
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
            <div class="select-parameter">
              <label for="blue_alignment">Alignment: {{ blue_team.Alignment }}</label>
              <br>
              <input type="range" id="blue_alignment" min="0" max="100" value="5" step="1" v-model="blue_team.Alignment">
            </div>
            <div class="select-parameter">
              <label for="blue_max_cost">Max Cost: {{ blue_team.Max_Cost }}</label>
              <br>
              <input type="range" id="blue_max_cost" min="20" max="100" value="5" step="5" v-model="blue_team.Max_Cost">
            </div>
          </div>
        </div>

        <!-- Red Team Settings -->
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
            <div class="select-parameter">
              <label for="red_alignment">Alignment: {{ red_team.Alignment }}</label>
              <br>
              <input type="range" id="red_alignment" class="accent" min="0" max="100" value="5" step="1" v-model="red_team.Alignment">
            </div>
          </div>
        </div>

        <!-- Green Node Settings -->
        <div class="flex-child green-team">
          <h2 id="greenTeam">Green Node Settings</h2>
          <div id="greenParameters">
            <div class="select-parameter">
              <label for="green_node_count_option">Green Node Configuration: </label>
              <select id="green_node_count_option" v-model="green_node_count_option">
                <option value="userData">User Data</option>
                <option value="userInput">User Input</option>
                <option value="random">Random</option>
              </select>
            </div>

            <div v-if="green_node_count_option === 'userInput'">
              <div class="select-parameter">
                <label for="green_node_count">Enter Number of Green Nodes:</label>
                <input type="number" id="green_node_count" v-model="green_nodes_count" min="1">
              </div>
              <div class="select-parameter">
                <label for="red_alignments">Red Alignment: {{ red_alignments }}%</label>
                <input type="range" id="red_alignments" v-model="red_alignments" min="0" max="100" step="10">
              </div>
              <div class="select-parameter">
                <label for="blue_alignments">Blue Alignment: {{ blue_alignments }}%</label>
                <input type="range" id="blue_alignments" v-model="blue_alignments" min="0" max="100" step="10">
              </div>
              <div class="select-parameter">
                <label for="green_alignments">Green (Neutral) Alignment: {{ green_alignments }}%</label>
                <input type="range" id="green_alignments" v-model="green_alignments" min="0" max="100" step="10" disabled>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button type="submit" class="submit-button">{{ green_node_count_option === 'userData' ? 'Next' : 'Start Simulation' }}</button>
    </form>

    <div v-if="display_params">
      <router-link to="/parameters" class="submit-button">View Parameters</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      models: ['gpt 3.5 turbo', 'custom'],
      blue_team: {
        Team: 'Blue',
        Model_ID: 'gpt 3.5 turbo',
        Energy: 50,
        Msgs_Generated: 5,
        Temperature: 0.5,
        Influence_Factor: 0.5,
        Alignment: 5,
        Max_Cost: 5,
      },
      red_team: {
        Team: 'Red',
        Model_ID: 'gpt 3.5 turbo',
        Energy: 50,
        Msgs_Generated: 5,
        Temperature: 0.5,
        Influence_Factor: 0.5,
        Alignment: 5,
        Max_Cost: 5,
      },
      green_node_count_option: 'userData',  // Default to user data
      green_nodes_count: 30, // Default to 30 green nodes
      red_alignments: 50,    // Default to 50% red alignments
      blue_alignments: 50,   // Default to 50% blue alignments
      green_alignments: 0,   // Automatically calculated as 100 - red_alignments - blue_alignments
      display_params: false,
    };
  },
  methods: {
    updateAlignments() {
      this.green_alignments = Math.max(0, 100 - this.red_alignments - this.blue_alignments);
    },
    async handleFormSubmit() {
      if (this.green_node_count_option === 'userData') {
        // Navigate to the FileUpload.vue page (assuming it's associated with the '/upload' route)
        this.$router.push('/upload');
      } else {
        const data = {
          red_team: this.red_team,
          blue_team: this.blue_team,
          green_node_count_option: this.green_node_count_option,
          green_nodes_count: this.green_nodes_count,
          red_alignments: this.red_alignments,
          blue_alignments: this.blue_alignments,
        };

        const path = 'http://127.0.0.1:5000/excel_api/ui_parameters';

        try {
          const response = axios.post(path, data);
          this.params = (await response).data;
          this.display_params = true;

          // Optional: Add a redirection after the successful simulation parameter set
          // this.$router.push('/parameters'); // This assumes you have a route for viewing the parameters.
        } catch (error) {
          console.log("Error: ", error);
        }
      }
    },
  }
};
</script>
