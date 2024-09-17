<template>
    <div v-if="display_error">
        <p>No parameters uploaded</p>
        <p>{{ errors }}</p>
        <router-link to="/">Upload parameters here</router-link>
    </div>

    <div v-else>
        <div class="container text-center">
            <!-- Current Round Display (Top of the View) -->
            <div class="current-round">
                <h3>Current Round: {{ currentRound }}</h3>
            </div>

            <div class="flex-container">
                <!-- Blue Team Display -->
                <div class="flex-child" id="game-view">
                    <div id="agents">
                        <h2 id="blueTeam">Blue Team</h2>
                        <div v-if="blue_team">
                            <p><span style="font-weight: bold;">Model: </span> {{ blue_team._model_ID }}</p>
                            <p><span style="font-weight: bold;">Alignment: </span> {{ blue_team._alignment }}</p>
                            <p><span style="font-weight: bold;">Energy Level: </span> {{ blue_team._energy }}</p>
                            <p><span style="font-weight: bold;">Influence Factor: </span> {{ blue_team._influence_factor }}</p>
                            <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ blue_team._message_count }}</p>
                            <p><span style="font-weight: bold;">Temperature</span> {{ blue_team._temperature }}</p>
                        </div>
                        <!--only display if winner has not been decided-->
                        <div v-if="blue_team_turn && !winner">
                            <button style="background-color: #0b7ffc; border: none" @click="nextTurn">Next round</button>
                        </div>
                    </div>
                </div>

                <!-- Network Graph Display -->
                <div class="flex-child" id="graph-view">
                    <!-- Add a ref to this div for proper graph rendering -->
                    <div ref="networkGraph" class="network-graph"></div>
                </div>

                <!-- Red Team Display -->
                <div class="flex-child" id="game-view">
                    <div id="agents">
                        <h2 id="redTeam">Red Team</h2>
                        <div v-if="red_team">
                            <p><span style="font-weight: bold;">Model: </span> {{ red_team._model_ID }}</p>
                            <p><span style="font-weight: bold;">Alignment: </span> {{ red_team._alignment }}</p>
                            <p><span style="font-weight: bold;">Influence Factor: </span> {{ red_team._influence_factor }}</p>
                            <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ red_team._message_count }}</p>
                            <p><span style="font-weight: bold;">Temperature</span> {{ red_team._temperature }}</p>
                        </div>
                        <!--only display if winner has not been decided-->
                        <div v-if="red_team_turn && !winner">
                            <button style="background-color: red; border: none" @click="nextTurn">Next round</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Message and Potency Display -->
            <div v-if="message && potency && !winner" id="Message">
                <p><span style="font-weight: bold;">Message: </span> {{ message }}</p>
                <p><span style="font-weight: bold;">Potency: </span> {{ potency }}</p>
                <button @click="downloadExcel" class="!py-20">Download Excel upon simulation end</button>
            </div>
            
            <!-- Winner Announcement -->
            <div v-if="winner">
                <h1>Winner: {{ winner }}</h1>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { drawNetworkGraph, fetchGraphDataForRound } from '@/services/graphDataService';

export default {
  data() {
    return {
      params: null,
      blue_team: null,
      red_team: null,
      display_error: false,
      errors: null,
      red_team_turn: true,
      blue_team_turn: false,
      message: null,
      potency: null,
      winner: null,
      currentRound: 0, // Track the current round number
    };
  },
  mounted() {
    this.getParameters();
    this.fetchAndDrawNetwork(this.currentRound); // Fetch and draw the initial network
  },
  methods: {
    downloadExcel() {
      axios({
        url: 'http://localhost:5000/excel_api/excel_export', 
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
    getParameters() {
      const path = 'http://127.0.0.1:5000/excel_api/get_parameters';
      axios.get(path)
        .then((response) => {
          if (response.data.length < 2) {
            this.display_error = true;
            this.errors = "No parameters uploaded";
            return;
          }

          this.red_team = response.data[0];
          this.blue_team = response.data[1];
        })
        .catch((error) => {
          console.error(error);
          this.display_error = true;
          this.errors = error;
        });
    },
    nextTurn() {
      const path = 'http://127.0.0.1:5000/excel_api/next_round';
      let team = '';
      if (this.red_team_turn) {
        team = 'red';
      } else {
        team = 'blue';
      }

      axios.get(`${path}?team=${team}`)
        .then((response) => {
          if (response.data.length < 2) {
            this.display_error = true;
            this.errors = "No parameters uploaded";
            return;
          }

          this.red_team_turn = !this.red_team_turn;
          this.blue_team_turn = !this.blue_team_turn;
          this.message = response.data[0];
          this.potency = response.data[1];
          this.winner = response.data[2];
          this.red_team = response.data[3];
          this.blue_team = response.data[4];

          // Increment the round number after each turn
          this.currentRound++;

          // Fetch and draw the network for the new round
          this.fetchAndDrawNetwork(this.currentRound);
        })
        .catch((error) => {
          console.error(error);
          this.display_error = true;
          this.errors = error;
        });
    },
    async fetchAndDrawNetwork(roundNumber) {
      try {
        const networkData = await fetchGraphDataForRound(roundNumber);
        if (this.$refs.networkGraph) {
          drawNetworkGraph(this.$refs.networkGraph, networkData);
        } else {
          console.error('Graph container not found.');
        }
      } catch (error) {
        console.error(`Error fetching or drawing network for round ${roundNumber}:`, error);
      }
    },
  }
};
</script>

<style scoped>
.current-round {
  margin-bottom: 20px; /* Space below the current round display */
  font-size: 1.2em;
}

.network-graph {
  width: 100%;
  height: 600px;
  border: 2px solid #ccc; /* Add border to the network graph */
  border-radius: 8px; /* Optional: Add rounded corners to the border */
  background-color: white; /* Optional: Add background color for better visibility */
}
</style>
