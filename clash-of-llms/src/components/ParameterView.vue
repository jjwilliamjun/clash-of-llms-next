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
                    <div v-if="blue_team">
                        <p><span style="font-weight: bold;">Model: </span> {{ blue_team._model_ID }}</p>
                        <p><span style="font-weight: bold;">Alignment: </span> {{ blue_team._alignment }}</p>
                        <p><span style="font-weight: bold;">Energy Level: </span> {{ blue_team._energy }}</p>
                        <p><span style="font-weight: bold;">Influence Factor: </span> {{ blue_team._influence_factor }}</p>
                        <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ blue_team._message_count }}</p>
                        <p><span style="font-weight: bold;">Temperature</span> {{ blue_team._temperature }}</p>
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
                </div>
            </div>
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
        errors: null
      };
    },
    mounted() {
        this.getParameters();
    },
    components: {
        NetworkGraph
    },
    methods: {
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
        }
    }
  };
</script>
