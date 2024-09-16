<template>
    <div v-if="display_error">
        <p>No parameters uploaded</p>
        <p>{{ errors }}</p>
        <router-link to="/">Upload parameters here</router-link>
    </div>

    <div v-else>
        <div class="container text-center">
            <div class="flex-container">

                <div class="flex-child" id="game-view">
                    <div id="agents">
                        <h2 id="blueTeam">Blue Team</h2>
                        <div v-if="blue_team && !winner">
                            <p><span style="font-weight: bold;">Model: </span> {{ blue_team._model_ID }}</p>
                            <p><span style="font-weight: bold;">Alignment: </span> {{ blue_team._alignment }}</p>
                            <p><span style="font-weight: bold;">Energy Level: </span> {{ blue_team._energy }}</p>
                            <p><span style="font-weight: bold;">Influence Factor: </span> {{ blue_team._influence_factor }}</p>
                            <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ blue_team._message_count }}</p>
                            <p><span style="font-weight: bold;">Temperature</span> {{ blue_team._temperature }}</p>
                            
                        </div>
                        <div v-if="blue_team_turn">
                            <button style="background-color: #0b7ffc;; border: none" @click="nextTurn">Next round</button>
                        </div>
                    </div>
                </div>

                <div class="flex-child" id="graph-view">
                    <NetworkGraph></NetworkGraph>
                </div>

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
                        <div v-if="red_team_turn && !winner">
                            <button style="background-color: red; border: none" @click="nextTurn">Next round</button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="message && potency && !winner" id="Message">
                <p><span style="font-weight: bold;">Message: </span> {{ message }}</p>
                <p><span style="font-weight: bold;">Potency: </span> {{ potency }}</p>
                <button @click="downloadExcel" class="!py-20">Download Excel upon simulation end</button>

            </div>
            <div v-if="winner">
                <h1>Winner: {{ winner }}</h1>
            </div>
        </div>
    </div>

</template>
  
<script>
import axios from 'axios';
import NetworkGraph from './NetworkGraph.vue';

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
        currentTeam:  null,
      };
    },
    mounted() {
        this.getParameters();
    },
    components: {
        NetworkGraph
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
            const path = 'http://127.0.0.1:5000/excel_api/get_parameters'
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
        nextTurn(){
            const path = 'http://127.0.0.1:5000/excel_api/next_round'
            let team = '';
            if (this.red_team_turn){
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
                })
                .catch((error) => {
                    console.error(error);
                    this.display_error = true;
                    this.errors = error;
            })
        }
    }
  };
</script>

