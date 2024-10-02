<template>
<div v-if="display_error">
    <p>No parameters uploaded</p>
    <p>{{ errors }}</p>
    <router-link to="/">Upload parameters here</router-link>
  </div>

  <div v-else>
    <div id="app" class="home">
      <h1>Confirm Parameter Selections:</h1>
      <div class="flex-container">
        <div class="flex-child">
          <h2 id="blueTeam">Blue Agent</h2>
          <div id="blueParameters">
            <div class="select-parameter">
              <div v-if="blue_team">
                <p>
                  <span style="font-weight: bold">Model: </span>
                  {{ blue_team._model_ID }}
                </p>
                <p>
                  <span style="font-weight: bold">Alignment: </span>
                  {{ blue_team._alignment }}%
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
                  <span style="font-weight: bold">Temperature: </span>
                  {{ blue_team._temperature }}
                </p>
                <p><span style="font-weight: bold;">Maximum Cost: </span> 
                  {{ blue_team._max_cost }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex-child">
          <h2 id="redTeam">Red Agent</h2>
          <div id="redParameters">
            <div class="select-parameter">
              <div v-if="red_team">
                <p>
                  <span style="font-weight: bold">Model: </span>
                  {{ red_team._model_ID }}
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
                <p>
                  <span style="font-weight: bold;">Penalise Messages with Potency of: </span>
                  {{ red_team._penalty_threshold }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex-child">
          <h2 id="greenTeam">Green Network</h2>
          <div id="greenParameters">
            <div class="select-parameter">
              <div v-if="green_team">
                <p>
                  <span style="font-weight: bold">Network Size: </span>
                  {{ green_team.size }}
                </p>
                <p>
                  <span style="font-weight: bold">Blue Aligned Nodes: </span>
                  {{ green_team.blue_alignment }}
                </p>
                <p>
                  <span style="font-weight: bold">Red Aligned Nodest: </span>
                  {{ green_team.red_alignment }}
                </p>
                <p>
                  <span style="font-weight: bold">Neutral Nodes: </span>
                  {{ green_team.neutral }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div>
            <div class="custom-box">
                <h2 class="condition-heading">Terminating conditions</h2>
                <div class="custom-conditions">
                    <div v-if="termination_conditions">
                        <p style="text-align: left"><span style="font-weight: bold;">Population alignment: </span> {{ termination_conditions.population_alignment }}%</p>
                        <p style="text-align: left"><span style="font-weight: bold;">Round number: </span> {{ termination_conditions.round_number }} </p>
                    </div>
                    </div>
                </div>
            </div>
      </div>
    <!-- </div> -->

    <h3>
      Once confirmed these settings are correct, select how you want to play and
      click "Start Simulation"
    </h3>

    <form @submit.prevent="submitGameStyle">
      <div class="option-toggle">
        <input
          type="radio"
          id="continuous"
          value="continuous"
          v-model="play_option"
        />
        <label for="continuous">Play Continuously</label>
        <input type="radio" id="turns" value="turns" v-model="play_option" />
        <label for="turns">Play in Turns</label>
      </div>
      <button type="submit" class="submit-button" @click="submitGameStyle">
        Start Simulation
      </button>
    </form>
    <div v-if="errors" id="errors">
      <p>Unable to start simulation: {{ errors }}</p>
    </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
      return {
        params: null,
        blue_team: null,
        red_team: null,
        green_team: null,
        display_error: false,
        errors: null,
        red_team_turn: true,
        blue_team_turn: false,
        message: null,
        potency: null,
        winner: null,
        currentTeam:  null,
        play_option: null,
        termination_conditions: null
      };
    },
    mounted() {
        this.getParameters();
    },
    methods: {
        downloadExcel() {
            axios({
                url: 'http://localhost:5000/excel_export', 
                method: 'GET',
                responseType: 'blob', 
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
            this.errors = `Error occurred when downloading excel file: ${
                error.response?.data?.error || error.message || error
            }`;
            this.$router.push({
                name: "error",
                query: {
                errorMessage: this.errors,
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
                    this.green_team = response.data[2];
                    this.termination_conditions = response.data[4];
                })
                .catch((error) => {
                    console.error(error);
                    this.display_error = true;
                    this.errors = error;
                });
    },
    async submitGameStyle() {
        const path = 'http://127.0.0.1:5000/set_gameplay';
        try {
            // Send selected option to backend
            const response = await axios.post(path, { play_option: this.play_option });
            if (response.status == 200) {
                this.$router.push('/gameplay');
            }
        } catch (error) {
            this.errors = `Error occurred when getting parameters: ${
                error.response?.data?.error || error.message || error
            }`;
            this.$router.push({
                name: "error",
                query: {
                    errorMessage: this.errors,
                },
            });
        }
    },
  },
};
</script>
