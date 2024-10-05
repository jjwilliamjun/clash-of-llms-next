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
            <h2 id="blueTeam">Blue Agent</h2>
            <div v-if="blue_team">
              <p>
                <span style="font-weight: bold">Model: </span>
                {{ blue_metadata ? blue_metadata.model_ID : blue_team._model_ID }}
              </p>
              <p>
                <span style="font-weight: bold">Alignment: </span>
                {{ blue_team._alignment }} %
              </p>
              <p>
                <span style="font-weight: bold">Energy Level: </span>
                {{ blue_team._energy }}
              </p>
              <p>
                <span style="font-weight: bold">Influence Factor: </span>
                {{ blue_team._influence_factor }}
              </p>
              <p>
                <span style="font-weight: bold"
                  >Number of Messages Generated Per Turn:
                </span>
                {{ blue_team._message_count }}
              </p>
              <p>
                <span style="font-weight: bold">Temperature</span>
                {{ blue_team._temperature }}
              </p>
            </div>
            <!--only display if winner has not been decided-->
            <div v-if="blue_team_turn && !termination_reason && !continuous">
              <button
                style="background-color: #0b7ffc; border: none"
                @click="nextTurn"
              >
                Next round
              </button>
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
            <h2 id="redTeam">Red Agent</h2>
            <div v-if="red_team">
              <p>
                <span style="font-weight: bold">Model: </span>
                {{ red_metadata ? red_metadata.model_ID : red_team._model_ID }}
              </p>
              <p>
                <span style="font-weight: bold">Alignment: </span>
                {{ red_team._alignment }} %
              </p>
              <p>
                <span style="font-weight: bold;">Penalty: </span> 
                {{ red_team._penalty }} %
              </p>
              <p>
                <span style="font-weight: bold">Influence Factor: </span>
                {{ red_team._influence_factor }}
              </p>
              <p>
                <span style="font-weight: bold"
                  >Number of Messages Generated Per Turn:
                </span>
                {{ red_team._message_count }}
              </p>
              <p>
                <span style="font-weight: bold">Temperature</span>
                {{ red_team._temperature }}
              </p>
            </div>
            <!--only display if winner has not been decided-->
            <div v-if="red_team_turn && !termination_reason && !continuous">
              <button
                style="background-color: red; border: none"
                @click="nextTurn"
              >
                Next round
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Message and Potency Display -->
      <div v-if="message && potency" id="Message">
        <div v-if="red_team_turn">
          <p>
            <span style="font-weight: bold">Blue Agent Message: </span>
            {{ message }}
          </p>
        </div>
        <div v-else>
          <p>
            <span style="font-weight: bold">Red Agent Message: </span>
            {{ message }}
          </p>
        </div>
        <!-- <p><span style="font-weight: bold;">Message: </span> {{ message }}</p> -->
                <div v-if="!red_team_turn && penalty_applied">
                  <p><span style="font-weight: bold;">Potency (Penalty Applied): </span> {{ red_team._potency }}</p>
                  <p><span style="font-weight: bold;">Original Potency (Before Penalty): </span> {{ red_team._unpenalised_potency }}</p>
                </div>
                <div v-else>
          <p><span style="font-weight: bold">Potency: </span> {{ potency }}</p>
                  <p><span style="font-weight: bold;">Energy Cost: </span> {{ blue_team._msg_cost }}</p>
                </div>
      </div>

      <!-- Winner Announcement -->
      <div id="app">
        <div v-if="termination_reason" class="popup">
          <div class="popup-inner">
            <div>
              <h1 v-if="victor "
                :id="
                  victor.toLowerCase() === 'red'
                    ? 'redTeam'
                    : victor.toLowerCase() === 'blue'
                    ? 'blueTeam'
                    : ''
                "
                class="font-bold mb-100"
              >
                Winner: {{ victor }}
              </h1>
              <h3 v-if="termination_reason" style="text-align: left;">End reason: {{ termination_reason }}</h3>
            </div>
            <div class="button-group">
              <router-link to="/">
                <button
                  class="home-button bg-green-500 text-white rounded hover:bg-green-600 transition"
                @click="cleanup">
                  <span>🏠</span> Home Page
                </button>
              </router-link>
              <button
                @click="downloadExcel"
                class="bg-blue-500 text-white rounded hover:bg-blue-600 transition"
              >
                Download Excel results
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  drawNetworkGraph,
  fetchGraphDataForRound,
} from "@/services/graphDataService";

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
      currentRound: 0, 
      game_style: null,
      blue_metadata: null,
      red_metadata: null,
      termination_conditions: null,
      termination_reason: null,
      victor: null,
      cors_errors: false,
      penalty_applied: false
    };
  },
  mounted() {
    this.getParameters();
    this.fetchAndDrawNetwork(this.currentRound); // Fetch and draw the initial network
  },
  methods: {
    downloadExcel() {
      axios({
        url: "http://127.0.0.1:5000/excel_export",
        method: "GET",
        responseType: "blob",
      })
        .then((response) => {
          const blob = new Blob([response.data], {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          });
          const link = document.createElement("a");

          link.href = window.URL.createObjectURL(blob);
          const now = new Date();
          const timestamp =
            now.getHours() + "_" + now.getMinutes() + "_" + now.getSeconds();

          const excel_file_name = `clash_of_llms_${timestamp}.xlsx`;
          link.download = excel_file_name;

          link.click();

          window.URL.revokeObjectURL(link.href);
        })
        .catch((error) => {
          console.error("Error downloading the Excel file:", error);
          this.errors = `Error downloading the Excel file: ${error.response?.data?.error || error.message || error}`;
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors || "An unexpected error occurred.",
            },
          });
        });
    },
    getParameters() {
      const path = "http://127.0.0.1:5000/get_parameters";
      axios
        .get(path)
        .then((response) => {
          if (response.data.length < 2) {
            this.display_error = true;
            this.errors = "No parameters uploaded";
            return;
          }

          this.red_team = response.data[0];
          this.blue_team = response.data[1];
          this.game_style = response.data[3];
          this.termination_conditions = response.data[4];
          this.continuous = this.game_style == "continuous";

          // Only fetch metadata if custom models are used
          if (this.red_team._model_ID === "custom") {
            this.getTeamMetadata("red");
          }
          if (this.blue_team._model_ID === "custom") {
            this.getTeamMetadata("blue");
          }
          if (this.continuous) {
            this.startContinuousGame();
            return;
          }
        })
        .catch((error) => {
          console.error(error);
          this.display_error = true;
          this.errors = error;
        });
    },
    getTeamMetadata(team) {
      const path = `http://127.0.0.1:5000/get_team_metadata/${team}`;
      axios
        .get(path)
        .then((response) => {
          if (team === "red") {
            this.red_metadata = response.data;
            this.red_team.metadata = response.data;
            this.red_team._model_ID = response.data.model_ID;  // Update the model ID
          } else if (team === "blue") {
            this.blue_metadata = response.data;
            this.blue_team.metadata = response.data;
            this.blue_team._model_ID = response.data.model_ID;  // Update the model ID
          }
        })
        .catch((error) => {
          console.error(`Error fetching ${team} team metadata:`, error);
        });
    },
    nextTurn() {
      const path = "http://127.0.0.1:5000/next_round";
      let team = "";
      if (this.red_team_turn) {
        team = "red";
      } else {
        team = "blue";
      }

      axios
        .get(`${path}?team=${team}`)
        .then((response) => {
          if (response.data.length < 2) {
            this.display_error = true;
            this.errors = "No parameters uploaded";
            return;
          }

          // Update teams and turns
          this.red_team_turn = !this.red_team_turn;
          this.blue_team_turn = !this.blue_team_turn;
          this.message = response.data.message;
          this.potency = response.data.potency;
          this.red_team = response.data.red_team;
          this.blue_team = response.data.blue_team;
          this.termination_reason = response.data.termination_reason;
          this.victor = response.data.victor;

          // Preserve custom model metadata and ensure the model ID remains from the metadata if it's custom
          if (this.red_team._model_ID === "custom" && this.red_metadata) {
            this.red_team._model_ID = this.red_metadata.model_ID;
          }
          if (this.blue_team._model_ID === "custom" && this.blue_metadata) {
            this.blue_team._model_ID = this.blue_metadata.model_ID;
          }

          if (!this.red_team_turn && this.red_team._potency !== this.red_team._unpenalised_potency) {
            this.penalty_applied = true;
          }

          // Increment the round number after each turn
          this.currentRound++;

          // Fetch and draw the network for the new round
          this.fetchAndDrawNetwork(this.currentRound);
        })
        .catch((error) => {
          console.error(error);
          this.errors = `Error occurred when running simulation: ${error.response?.data?.error || error.message || error}`;
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors || "An unexpected error occurred.",
            },
          });
        });
    },
    cleanup(){
        const path = "http://127.0.0.1:5000/cleanup";
        axios
        .get(path)
        .then((response) => {
          if (response.data.length < 2) {
            this.display_error = true;
            this.errors = "No parameters uploaded";
            return;
          }

          this.red_team = response.data[0];
          this.blue_team = response.data[1];
          this.game_style = response.data[3];
          this.termination_conditions = response.data[4];
          this.continuous = this.game_style == "continuous";

          if (this.continuous) {
            this.startContinuousGame();
            return;
          }
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
          console.error("Graph container not found.");
        }
      } catch (error) {
        this.errors = `Error occurred when displaying network: ${error.response?.data?.error || error.message || error}`;
        console.error(
          `Error fetching or drawing network for round ${roundNumber}:`,
          error
        );
        this.$router.push({
          name: "error",
          query: {
            errorMessage: this.errors,
          },
        });
      }
    },
    async startContinuousGame() {
      const path = "http://127.0.0.1:5000/continuous_game";

      while (this.red_team_turn || this.blue_team_turn) {
        try {
            const response = await axios.get(path);
                this.red_team_turn = !this.red_team_turn;
                this.blue_team_turn = !this.blue_team_turn;
                this.message = response.data.message;
                console.log(this.message)
                this.potency = response.data.potency;
                this.red_team = response.data.red_team;
                this.blue_team = response.data.blue_team;
                this.termination_reason = response.data.termination_reason;
                this.victor = response.data.victor;

          this.red_team_turn = !this.red_team_turn;
          this.blue_team_turn = !this.blue_team_turn;
          this.message = response.data.message;
          this.potency = response.data.potency;
          this.winner = response.data.victor;
          this.red_team = response.data.red_team;
          this.blue_team = response.data.blue_team;

          // Preserve custom model metadata
          if (this.red_team._model_ID === "custom" && this.red_metadata) {
            this.red_team._model_ID = this.red_metadata.model_ID;
          }
          if (this.blue_team._model_ID === "custom" && this.blue_metadata) {
            this.blue_team._model_ID = this.blue_metadata.model_ID;
          }

          if (!this.red_team_turn && this.red_team._potency !== this.red_team._unpenalised_potency) {
            this.penalty_applied = true;
            console.log("Penalty applied: ", this.red_team._potency, this.red_team._unpenalised_potency);
          }
            // Increment the round number after each turn
            this.currentRound++;

            // Fetch and draw the network for the new round
            this.fetchAndDrawNetwork(this.currentRound);
        } catch (error) {
          console.error(error);
          this.errors = `Error occurred when running continuous simulation: ${error.response?.data?.error || error.message || error}`;
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors,
            },
          });
          return;
        }
            if (this.victor == 'red' || this.victor == 'blue') {
                return;
            }
                
            // Wait 25 seconds before next round - chatgpt query takes time
            await new Promise(resolve => setTimeout(resolve, 15000));
        }
         return;
        }
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
  height: 500px;
  border: 2px solid #ccc; /* Add border to the network graph */
  border-radius: 8px; /* Optional: Add rounded corners to the border */
  background-color: white; /* Optional: Add background color for better visibility */
}
.home-button {
  background-color: #1d6e30;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}
.popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;

  .popup-inner {
    width: 300px;
    height: 200px;
    background: #fff;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    padding: 40px;
    border-radius: 10px;
  }

  .popup-inner h1 {
    margin-bottom: 100px;
    text-align: center;
  }

  .button-group {
    float:inline-end;
    display: flex;
    gap: 8px;
    padding: 20px;
  }
}
</style>
