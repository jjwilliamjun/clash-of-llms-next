<template>
  <div class="container">
    <!-- Sticky Sidebar Navigation -->
    <nav class="sticky-sidebar">
      <ul>
        <li><a href="javascript:void(0)" @click="scrollToSection('project-description')">Project Description</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('importing-files')">Importing Files</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('simulation-settings')">Simulation Settings</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('custom-llm-guide')">Custom LLM Guide</a></li> <!-- New Section -->
        <li><a href="javascript:void(0)" @click="scrollToSection('node-connections')">Node Connections</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('node-attributes')">Node Attributes</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('export-simulation-data')">Export Simulation Data</a></li>
      </ul>
    </nav>

    <!-- Content Area -->
    <div class="content-area">
      <!-- Loading State -->
      <div v-if="loading" class="loading">Loading...</div>

      <!-- Project Description Section -->
      <section id="project-description" v-if="!loading && projectDescription">
        <h1>{{ projectDescription.title }}</h1>
        <div v-for="section in projectDescription.sections" :key="section.subtitle">
          <h3>{{ section.subtitle }}</h3>
          <p v-html="section.content"></p>
        </div>
      </section>

      <!-- Importing Files Section -->
      <section id="importing-files" v-if="!loading && guideData.importingFiles">
        <h2>{{ guideData.importingFiles.title }}</h2>
        <ol>
          <li v-for="step in guideData.importingFiles.steps" :key="step">{{ step }}</li>
        </ol>
      </section>

      <!-- Simulation Settings Section -->
      <section id="simulation-settings" v-if="!loading && guideData.simulationSettings">
        <h1>{{ guideData.simulationSettings.title }}</h1>
        <h3>{{ guideData.simulationSettings.overview.title }}</h3>
        <p>{{ guideData.simulationSettings.overview.content }}</p>

        <!-- Simulation Settings Structure Table -->
        <h3>{{ guideData.simulationSettings.structure.title }}</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in guideData.simulationSettings.structure.tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in guideData.simulationSettings.structure.tableContent" :key="row[0]">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Energy Explanation -->
        <h3>{{ guideData.simulationSettings.energyExplanation.title }}</h3>
        <p>{{ guideData.simulationSettings.energyExplanation.content }}</p>

        <!-- Msgs Generated Explanation -->
        <h3>{{ guideData.simulationSettings.msgsGeneratedExplanation.title }}</h3>
        <p>{{ guideData.simulationSettings.msgsGeneratedExplanation.content }}</p>

        <!-- Temperature Explanation -->
        <h3>{{ guideData.simulationSettings.temperatureExplanation.title }}</h3>
        <p>{{ guideData.simulationSettings.temperatureExplanation.content }}</p>

        <!-- Simulation Settings Example Table -->
        <h3>{{ guideData.simulationSettings.example.title }}</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in guideData.simulationSettings.example.tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in guideData.simulationSettings.example.tableContent" :key="row[0]">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Instructions -->
        <h3>{{ guideData.simulationSettings.instructions.title }}</h3>
        <ul>
          <li v-for="instruction in guideData.simulationSettings.instructions.content" :key="instruction">{{ instruction }}</li>
        </ul>
        <!-- Download Simulation Settings Example -->
        <div class="download-section">
          <h3>Download Example File</h3>
          <a href="/documents/SimulationSettings.xlsx" download="SimulationSettings.xlsx">SimulationSettings.xlsx</a>
        </div>
      </section>
      
      <!-- Custom LLM Guide Section -->
      <section id="custom-llm-guide" v-if="!loading && customLLMGuide">
        <h1>{{ customLLMGuide.title }}</h1>
        <p>{{ customLLMGuide.description }}</p>
        
        <!-- Steps to create Custom LLM File -->
        <div v-for="step in customLLMGuide.steps" :key="step.title">
          <h3>{{ step.title }}</h3>
          <ul>
            <li v-for="(content, index) in step.content" :key="index">
              <template v-if="typeof content === 'string'">
                {{ content }}
              </template>
              <template v-else>
                <pre>{{ JSON.stringify(content.template, null, 2) }}</pre>
              </template>
            </li>
          </ul>
        </div>
        <!-- Download Simulation Settings Example -->
        <div class="download-section">
          <h3>Download Example File</h3>
          <a href="/documents/simple_pytorch_model.pt" download="simple_pytorch_model.pt">simple_pytorch_model.pt</a>
        </div>
      </section>      

      <!-- Node Connections Section -->
      <section id="node-connections" v-if="!loading && guideData.nodeConnections">
        <h1>{{ guideData.nodeConnections.title }}</h1>
        <h3>{{ guideData.nodeConnections.overview.title }}</h3>
        <p>{{ guideData.nodeConnections.overview.content }}</p>

        <!-- Node Connections Structure Table -->
        <h3>{{ guideData.nodeConnections.structure.title }}</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in guideData.nodeConnections.structure.tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in guideData.nodeConnections.structure.tableContent" :key="row[0]">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Example for Node Connections -->
        <h3>{{ guideData.nodeConnections.example.title }}</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in guideData.nodeConnections.example.tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in guideData.nodeConnections.example.tableContent" :key="row[0]">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Instructions -->
        <h3>{{ guideData.nodeConnections.instructions.title }}</h3>
        <ul>
          <li v-for="instruction in guideData.nodeConnections.instructions.content" :key="instruction">{{ instruction }}</li>
        </ul>

        <!-- Tips -->
        <h3>{{ guideData.nodeConnections.tips.title }}</h3>
        <ul>
          <li v-for="tip in guideData.nodeConnections.tips.content" :key="tip">{{ tip }}</li>
        </ul>
        <!-- Download Node Connections Example -->
        <div class="download-section">
          <h3>Download Example File</h3>
          <a href="/documents/NodeConnections.xlsx" download="NodeConnections.xlsx">NodeConnections.xlsx</a> 
        </div>  
      </section>

      <!-- Node Attributes Section -->
      <section id="node-attributes" v-if="!loading && guideData.nodeAttributes">
        <h1>{{ guideData.nodeAttributes.title }}</h1>
        <h3>{{ guideData.nodeAttributes.overview.title }}</h3>
        <p>{{ guideData.nodeAttributes.overview.content }}</p>
        <!-- Alignment Explanation -->
        <h3>{{ guideData.nodeAttributes.alignmentExplanation.title }}</h3>
        <ul>
          <li v-for="alignment in guideData.nodeAttributes.alignmentExplanation.content" :key="alignment.range">
            <strong>{{ alignment.range }}:</strong> {{ alignment.description }}
          </li>
        </ul>


        <!-- Node Attributes Example Table -->
        <h3>{{ guideData.nodeAttributes.example.title }}</h3>
        <table>
          <thead>
            <tr>
              <th v-for="header in guideData.nodeAttributes.example.tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in guideData.nodeAttributes.example.tableContent" :key="row[0]">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Instructions -->
        <h3>{{ guideData.nodeAttributes.instructions.title }}</h3>
        <ul>
          <li v-for="instruction in guideData.nodeAttributes.instructions.content" :key="instruction">{{ instruction }}</li>
        </ul>

        <!-- Tips -->
        <h3>{{ guideData.nodeAttributes.tips.title }}</h3>
        <ul>
          <li v-for="tip in guideData.nodeAttributes.tips.content" :key="tip">{{ tip }}</li>
        </ul>

        <!-- Download Node Attributes Example -->
        <div class="download-section">
          <h3>Download Example File</h3>
          <a href="/documents/NodeAttributes.xlsx" download="NodeAttributes.xlsx">NodeAttributes.xlsx</a>
        </div>
        
      </section>

      <!-- Export Simulation Data Section -->
      <section id="export-simulation-data" v-if="!loading && exportSimulationData">
        <h1>{{ exportSimulationData.title }}</h1>
      
        <!-- Introduction -->
        <div v-if="exportSimulationData.introduction">
          <h2>{{ exportSimulationData.introduction.title }}</h2>
          <p>{{ exportSimulationData.introduction.content }}</p>
        </div>
      
        <!-- Columns Description -->
        <div v-if="exportSimulationData.columnsDescription">
          <h2>{{ exportSimulationData.columnsDescription.title }}</h2>
          <ul>
            <li v-for="column in exportSimulationData.columnsDescription.content" :key="column.columnName">
              <strong>{{ column.columnName }}:</strong> {{ column.description }}
            </li>
          </ul>
        </div>
      
        <!-- Example Table -->
        <div v-if="exportSimulationData.exampleTable">
          <h2>{{ exportSimulationData.exampleTable.title }}</h2>
          <p>{{ exportSimulationData.exampleTable.description }}</p>
          <table class="export-simulation-table">
            <thead>
              <tr>
                <th v-for="header in exportSimulationData.exampleTable.headers" :key="header">{{ header }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in exportSimulationData.exampleTable.exampleData" :key="row[0]">
                <td v-for="cell in row" :key="cell">{{ cell }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      guideData: {},              // For storing data from guide.json (Excel Guide)
      projectDescription: null,   // For storing data from project_description.json
      exportSimulationData: null, // For storing data from export_simulation.json
      customLLMGuide: null,       // For storing data from custom_llm_option.json
      loading: true               // Loading state
    };
  },
  mounted() {
    this.fetchAllData();
  },
  methods: {
    // Fetch all necessary data
    async fetchAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.fetchProjectDescription(),
          this.fetchGuideData(),
          this.fetchExportSimulationData(),
          this.fetchCustomLLMGuide() // Fetch the custom LLM guide
        ]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchProjectDescription() {
      try {
        const response = await axios.get('/documents/project_description.json');
        this.projectDescription = response.data;
      } catch (error) {
        console.error('Error fetching project description:', error);
      }
    },

    async fetchGuideData() {
      try {
        const response = await axios.get('/documents/guide.json');
        this.guideData = response.data;
      } catch (error) {
        console.error('Error fetching guide data:', error);
      }
    },

    async fetchExportSimulationData() {
      try {
        const response = await axios.get('/documents/export_simulation.json');
        this.exportSimulationData = response.data;
      } catch (error) {
        console.error('Error fetching export simulation data:', error);
      }
    },

    async fetchCustomLLMGuide() {
      try {
        const response = await axios.get('/documents/custom_llm_option.json');
        this.customLLMGuide = response.data.custom_llm_guide;
      } catch (error) {
        console.error('Error fetching custom LLM guide:', error);
      }
    },

    // Method to scroll to the section smoothly
    scrollToSection(sectionId) {
      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }
};
</script>


<style scoped>
.container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
}

.sticky-sidebar {
  position: -webkit-sticky; /* For Safari */
  position: sticky;
  top: 20px;
  width: 200px;
  height: 100%; /* Ensure full height for long scrolling */
  padding: 20px;
  background: #f9f9f9;
  border-right: 1px solid #ddd;
}

nav ul {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
  text-align: left; /* Ensure alignment for the sidebar */
}

nav ul li {
  margin-bottom: 15px;
}

nav ul li a {
  text-decoration: none;
  color: #007BFF;
  font-weight: bold;
  text-align: left; /* Sidebar links aligned to the left */
}

nav ul li a:hover,
nav ul li a:focus {
  text-decoration: underline;
}

/* Content area for sections */
.content-area {
  margin: 0 auto; /* Center the content area */
  padding: 20px;
  flex: 1;
  max-width: 800px; /* Set a maximum width for the content */
}

html {
  scroll-behavior: smooth;
}

/* Add space between sections */
section {
  margin-bottom: 40px; /* Increase space between each section */
}

h2, h3, p, table, ol, ul {
  text-align: left;
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  font-size: 30px;
  margin-bottom: 15px;
  text-align: center; /* Align headings left */
}

h2 {
  font-size: 24px;
  margin-bottom: 15px;
  text-align: left; /* Align headings left */
}

h3 {
  font-size: 20px; /* Adjusted size for better hierarchy */
  margin-bottom: 12px;
  text-align: left; /* Align sub-headings left */
}

h4 {
  font-size: 18px;
  margin-bottom: 10px;
  text-align: left; /* Align h4 left */
}

p {
  font-size: 16px;
  margin-bottom: 20px;
  max-width: 800px;
  line-height: 1.6;
  word-break: break-word;
  overflow-wrap: break-word;
  text-align: left; /* Ensure paragraphs are aligned left */
}

/* Updated table styling for better readability */
table {
  width: 100%;
  max-width: 1000px;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  table-layout: auto; /* Ensures that the table has consistent column widths */
  word-wrap: break-word;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px 8px;
  text-align: left; /* Ensure table cells and headers are aligned left */
  word-break: break-word;
  overflow-wrap: break-word;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
  font-size: 14px; /* Make the text a bit smaller for better readability */
  text-align: left; /* Ensure table headers are aligned left */
}

td {
  font-size: 14px;
  text-align: left; /* Ensure table cells are aligned left */
}

/* Widen the first column */
th:first-child, td:first-child {
  width: 25%; /* Adjust this value to make the first column wider */
}

/* Widen the third column */
th:nth-child(3), td:nth-child(3) {
  width: 18%; /* Adjust this value to make the third column wider */
}


tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* Export Simulation Table Styles */
.export-simulation-table {
  width: 100%;
  max-width: 1000px;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.export-simulation-table th, .export-simulation-table td {
  border: 1px solid #ddd;
  padding: 12px 8px;
  text-align: left;
}

/* Adjust column widths for Export Simulation Table */
.export-simulation-table th:first-child, .export-simulation-table td:first-child {
  width: 10%; /* Adjust this value to balance the first column */
}

.export-simulation-table th:nth-child(2), .export-simulation-table td:nth-child(2) {
  width: 10%; /* Adjust width for the 'Team' column */
}

.export-simulation-table th:nth-child(3), .export-simulation-table td:nth-child(3) {
  width: 20%; /* Adjust width for the 'Message Chosen' column */
}

.export-simulation-table th:nth-child(4), .export-simulation-table td:nth-child(4) {
  width: 12%; /* Adjust width for 'Potency' column */
}

.export-simulation-table th:nth-child(5), .export-simulation-table td:nth-child(5) {
  width: 10%; /* Adjust width for 'Energy Level' column */
}

.export-simulation-table th:nth-child(6), .export-simulation-table td:nth-child(6) {
  width: 20%; /* Adjust width for 'Increased Alignment' column */
}

.export-simulation-table th:nth-child(7), .export-simulation-table td:nth-child(7) {
  width: 20%; /* Adjust width for 'Decreased Alignment' column */
}

/* Add a background color for even rows in the Export Simulation Table */
.export-simulation-table tr:nth-child(even) {
  background-color: #f9f9f9;
}


ol, ul {
  margin-left: 20px;
  margin-bottom: 20px;
  max-width: 800px;
  word-break: break-word;
  overflow-wrap: break-word;
  text-align: left; /* Ensure lists are aligned left */
}

.loading {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-top: 50px;
}

html {
  scroll-behavior: smooth;
}

/* Add this to your style section */
.download-section {
  text-align: left; /* Aligns text to the left */
  margin-top: 20px; /* Add some margin if needed */
}

/* You can also apply this rule directly to h3 and a if needed */
.download-section h3,
.download-section a {
  display: block; /* Makes sure each element starts on a new line */
  margin: 0; /* Remove any default margin */
  text-align: left; /* Aligns text to the left */
}


</style>

