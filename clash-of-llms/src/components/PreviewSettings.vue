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
                                <p><span style="font-weight: bold;">Model: </span> {{ blue_team._model_ID }}</p>
                                <p><span style="font-weight: bold;">Alignment: </span> {{ blue_team._alignment }}%</p>
                                <p><span style="font-weight: bold;">Energy Level: </span> {{ blue_team._energy }}</p>
                                <p><span style="font-weight: bold;">Influence Factor: </span> {{ blue_team._influence_factor }}</p>
                                <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ blue_team._message_count }}</p>
                                <p><span style="font-weight: bold;">Temperature: </span> {{ blue_team._temperature }}</p>  
                                <p><span style="font-weight: bold;">Maximum Cost: </span> {{ blue_team._max_cost }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex-child">
                    <h2 id="redTeam">Red Agent</h2>
                    <div id="redParameters">
                        <div class="select-parameter">
                            <div v-if="red_team">
                            <p><span style="font-weight: bold;">Model: </span> {{ red_team._model_ID }}</p>
                            <p><span style="font-weight: bold;">Alignment: </span> {{ red_team._alignment }} %</p>
                            <p><span style="font-weight: bold;">Penalty: </span> {{ red_team._penalty }} %</p>
                            <p><span style="font-weight: bold;">Influence Factor: </span> {{ red_team._influence_factor }}</p>
                            <p><span style="font-weight: bold;">Number of Messages Generated Per Turn: </span> {{ red_team._message_count }}</p>
                            <p><span style="font-weight: bold;">Temperature</span> {{ red_team._temperature }}</p>
                            <p><span style="font-weight: bold;">Penalise Messages with Potency of: </span> {{ red_team._penalty_threshold }}</p>
                        </div>
                        </div>
                    </div>
                </div>

                <div class="flex-child">
                    <h2 id="greenTeam">Green Network</h2>
                    <div id="greenParameters">
                        <div class="select-parameter">
                            <div v-if="green_team">
                                <p><span style="font-weight: bold;">Network Size: </span> {{ green_team.size }}</p>
                                <p><span style="font-weight: bold;">Blue Aligned Nodes: </span> {{ green_team.blue_alignment }} </p>
                                <p><span style="font-weight: bold;">Red Aligned Nodest: </span> {{ green_team.red_alignment }}</p>
                                <p><span style="font-weight: bold;">Neutral Nodes: </span> {{ green_team.neutral }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <!-- </div> -->

        <h3>Once confirmed these settings are correct, select how you want to play and click "Start Simulation"</h3>

            <form @submit.prevent="submitGameStyle">
                <div class="option-toggle">
                    <input type="radio" id="continuous" value="continuous" v-model="play_option" />
                    <label for="continuous">Play Continuously</label>
                    <input type="radio" id="turns" value="turns" v-model="play_option" />
                    <label for="turns">Play in Turns</label>
                </div>
                <button type="submit" class="submit-button" @click="submitGameStyle">Start Simulation</button>
            </form>
            <div v-if="errors" id="errors">
                <p>Unable to start simulation: {{ errors }}</p>
            </div>
        </div>
    </div>

</template>
  
<script>
import axios from 'axios';

export default {
    data() {
      return {
        params: null,
        blue_team: null,
        red_team: null,
        green_team: null,
        display_error: false,
        errors: null,
        play_option: null
      };
    },
    mounted() {
        this.getParameters();
    },
    methods: {
        getParameters() {
            const path = 'http://127.0.0.1:5000/get_parameters';
            axios.get(path)
                .then((response) => {
                    if (response.data.length < 2) {
                        this.display_error = true;
                        this.errors = "No parameters uploaded";
                        return;
                    }

                    this.red_team = response.data[0];
                    this.blue_team = response.data[1];
                    this.green_team = response.data[2];
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
                this.errors = error.response.data.error;
            }
        }
    }
};
</script>

