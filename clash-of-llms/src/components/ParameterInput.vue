<template>
  <div>
    <!-- Form -->
    <form @submit.prevent="handleFormSubmit">
      <div class="flex-container">
        <!-- Blue Team Settings -->
        <div class="flex-child">
          <h2 id="blueTeam">Blue Agent</h2>
          <div id="blueParameters">
            <div class="select-parameter">
              <label for="blue_model">Model: </label>
              <div class="styled-select">
                <select name="blue_model" v-model="blue_team.Model_ID">
                  <option v-for="(item, index) in models" :key="index" :value="item">{{ item }}</option>
                </select>
              </div>  
            </div>

            <!-- File Upload for Custom Model -->
            <div v-if="blue_team.Model_ID === 'custom'" class="select-parameter">
              <label for="file_upload_blue">Upload Custom File:</label>
              <input type="file" id="file_upload_blue" class="hidden-input" @change="handleFileUploadBlue" />
              <button type="button" class="custom-upload-btn-blue" @click="triggerFileUpload('file_upload_blue')">Choose File</button>
              <span id="file-upload-blue-name">{{ blue_team.Custom_File ? blue_team.Custom_File.name : 'No file chosen' }}</span>
            </div>

            <!-- Existing Parameters -->
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
              <label for="blue_max_cost">Maximum Energy Cost of Messages: {{ blue_team.Max_Cost }}</label>
              <br>
              <input type="range" id="blue_max_cost" min="5" max="100" value="5" step="1" v-model="blue_team.Max_Cost">
            </div>
          </div>
        </div>

        <!-- Red Team Settings -->
        <div class="flex-child">
          <h2 id="redTeam">Red Agent</h2>
          <div id="redParameters">
            <div class="select-parameter">
              <label for="red_model">Model: </label>
              <div class="styled-select">
                <select name="red_model" v-model="red_team.Model_ID">
                  <option v-for="(item, index) in models" :key="index" :value="item">{{ item }}</option>
                </select>
              </div>  
            </div>

            <!-- File Upload for Custom Model (Red Team) -->
            <div v-if="red_team.Model_ID === 'custom'" class="select-parameter">
              <label for="file_upload_red">Upload Custom File:</label>
              <input type="file" id="file_upload_red" class="hidden-input" @change="handleFileUploadRed" />
              <button type="button" class="custom-upload-btn-red" @click="triggerFileUpload('file_upload_red')">Choose File</button>
              <span id="file-upload-red-name">{{ red_team.Custom_File ? red_team.Custom_File.name : 'No file chosen' }}</span>
            </div>

            <!-- Existing Parameters -->
            <div class="select-parameter">
              <label for="red_penalty">Penalty: {{ red_team.Penalty }} %</label>
              <br>
              <input type="range" id="red_penalty" class="accent" max="100" value="50" step="1" v-model="red_team.Penalty">
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
              <label for="red_penalty">Penalise Messages with Potencies over: {{ red_team.Penalty_Threshold }}</label>
              <br>
              <input type="range" id="red_penalty" class="accent" max="100" value="50" step="1" v-model="red_team.Penalty_Threshold">
            </div>
          </div>
        </div>

        <!-- Green Node Settings -->
        <div class="flex-child green-team">
          <h2 id="greenTeam">Population</h2>
          <div id="greenParameters">
            <div class="select-parameter">
              <label for="green_node_count_option">Population Configuration: </label>
              <div class="styled-select">
                <select id="green_node_count_option" v-model="green_node_count_option">
                  <option value="userData">User Data</option>
                  <option value="userInput">User Input</option>
                  <option value="random">Random</option>
                </select>
              </div>
            </div>

            <div v-if="green_node_count_option === 'userInput'">
              <div class="select-parameter">
                <label for="green_node_count">Enter Number of Green Nodes:</label>
                <input type="number" id="green_node_count" v-model="green_nodes_count" min="1">
              </div>
              <div class="select-parameter">
                <label for="red_alignments">Red Alignment: {{ red_alignments }}%</label>
                <input type="range" id="red_alignments" class="accent" v-model="red_alignments" min="0" max="100" step="10">
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
      <div class="condition-box">
        <h2 class="condition-heading">Terminating Conditions</h2>
        <div class="custom-conditions">
            <div class="select-parameter">
                <label for="population_alignments">Population Alignment: {{ population_alignment }}%</label>
                <input type="range" class="condition-accent" v-model="population_alignment" min="0" max="100" step="5">
            </div>
            <div class="select-parameter">
                <label for="round_number">Round number: {{ round_number }}</label>
                <input type="range" class="condition-accent" v-model="round_number" min="0" max="50" step="1">
            </div>
        </div>
      </div>
      <button type="submit" class="submit-button">{{ green_node_count_option === 'userData' ? 'To Excel File Upload' : 'Next' }}</button>
    </form>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      models: ['gpt-4o-mini', 'gpt-4o', 'gpt-4o-turbo', 'gpt-3.5-turbo', 'custom'],
      blue_team: {
        Team: 'Blue',
        Model_ID: 'gpt-4o-mini',
        Custom_Model: '',
        Energy: 50,
        Msgs_Generated: 5,
        Temperature: 0.5,
        Influence_Factor: 0.5,
        Alignment: 50,
        Max_Cost: 20,
        Custom_File: null, // New property to store the uploaded file for the blue team
        Penalty: 50,
        Penalty_Threshold: 50
      },
      red_team: {
        Team: 'Red',
        Model_ID: 'gpt-4o-mini',
        Custom_Model: '',
        Energy: 50,
        Msgs_Generated: 5,
        Temperature: 0.5,
        Influence_Factor: 0.5,
        Alignment: 50,
        Max_Cost: 20,
        Custom_File: null, // New property to store the uploaded file for the red team
        Penalty: 50,
        Penalty_Threshold: 50

      },
      green_node_count_option: 'userData',
      green_nodes_count: 30,
      red_alignments: 50,
      blue_alignments: 50,
      green_alignments: 0,
      display_params: false,
      errors: null,

      // Custom terminating conditions
      population_alignment: 80,
      round_number: 20,
    };
  },
  computed: {
    showFileUpload() {
      return this.red_team.Model_ID === 'custom' || this.blue_team.Model_ID === 'custom';
    }
  },
  methods: {
    updateAlignments() {
      this.green_alignments = Math.max(0, 100 - this.red_alignments - this.blue_alignments);
    },
    triggerFileUpload(inputId) {
      document.getElementById(inputId).click();
    },
    handleFileUploadBlue(event) {
      const file = event.target.files[0];
      this.blue_team.Custom_File = file;
    },
    handleFileUploadRed(event) {
      const file = event.target.files[0];
      this.red_team.Custom_File = file;
    },
    async uploadLLMFiles() {
      const uploadPromises = [];

      if (this.blue_team.Model_ID === 'custom' && this.blue_team.Custom_File) {
        const formData = new FormData();
        formData.append('llm_file', this.blue_team.Custom_File);
        formData.append('team', 'blue');
        uploadPromises.push(
          axios.post('http://127.0.0.1:5000/upload_llm', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        );
      }

      if (this.red_team.Model_ID === 'custom' && this.red_team.Custom_File) {
        const formData = new FormData();
        formData.append('llm_file', this.red_team.Custom_File);
        formData.append('team', 'red');
        uploadPromises.push(
          axios.post('http://127.0.0.1:5000/upload_llm', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        );
      }

      try {
        await Promise.all(uploadPromises);
      } catch (error) {
        console.error("Error uploading LLM files:", error.response ? error.response.data : error.message);
        throw error;
      }
    },
    async handleFormSubmit() {
      try {
        if (this.green_node_count_option === 'userData') {
          this.$router.push('/upload');
          return;
        }

        if (this.green_node_count_option === 'userInput') {
          this.red_team.Alignment = this.red_alignments;
          this.blue_team.Alignment = this.blue_alignments;
        }

        if (this.showFileUpload) {
          if (!this.blue_team.Custom_File && this.blue_team.Model_ID === 'custom') {
            throw new Error("Please upload a custom file for Blue Team.");
          }
          if (!this.red_team.Custom_File && this.red_team.Model_ID === 'custom') {
            throw new Error("Please upload a custom file for Red Team.");
          }

          await this.uploadLLMFiles();
        }

        this.red_team.Alignment = this.red_alignments;
        this.blue_team.Alignment = this.blue_alignments;

        const data = {
          red_team: {
            ...this.red_team,
            Custom_Model: this.red_team.Model_ID === 'custom' ? this.red_team.Custom_Model : ''
          },
          blue_team: {
            ...this.blue_team,
            Custom_Model: this.blue_team.Model_ID === 'custom' ? this.blue_team.Custom_Model : ''
          },
          green_node_count_option: this.green_node_count_option,
          green_nodes_count: this.green_nodes_count,
          red_alignments: this.red_alignments,
          blue_alignments: this.blue_alignments,

          // custom terminating conditions
          population_alignment: this.population_alignment,
          round_number: this.round_number,
        };

        const response = await axios.post('http://127.0.0.1:5000/ui_parameters', data);
        this.params = response.data;
        this.display_params = true;

        
        if (this.blue_team.Model_ID === 'custom') {
          this.blue_team.Model_ID = 'custom';
        }
        if (this.red_team.Model_ID === 'custom') {
          this.red_team.Model_ID = 'custom';
        }
        
        this.$router.push('/preview'); // Uncomment if you want to redirect to parameters view

      } catch (error) {
        console.error("Error submitting form:", error.response ? error.response.data : error.message);
        this.errors = `Error submitting form: ${
            error.response?.data?.error || error.message || error
          }`;
          this.$router.push({
            name: "error",
            query: {
              errorMessage: this.errors,
            },
          });
      }
    }
  },
  watch: {
    red_alignments: 'updateAlignments',
    blue_alignments: 'updateAlignments',
  }
};
</script>


