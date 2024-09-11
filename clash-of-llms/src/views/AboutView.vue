<template>
  <div class="container">
    <!-- Sticky Sidebar Navigation -->
    <nav class="sticky-sidebar">
      <ul>
        <li><a href="javascript:void(0)" @click="scrollToSection('project-description')">Project Description</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('importing-files')">Importing Files</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('simulation-settings')">Simulation Settings</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('export-simulation-data')">Export Simulation Data</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('node-connections')">Node Connections</a></li>
        <li><a href="javascript:void(0)" @click="scrollToSection('node-attributes')">Node Attributes</a></li>
      </ul>
    </nav>

    <!-- Content Area -->
    <div class="content-area">
      <!-- Loading State -->
      <div v-if="loading" class="loading">Loading...</div>

      <!-- Project Description Section -->
      <section id="project-description" v-if="!loading && projectDescription">
        <h2>{{ projectDescription.title }}</h2>
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
        <h2>{{ guideData.simulationSettings.title }}</h2>
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
      </section>

      <!-- Node Connections Section -->
      <section id="node-connections" v-if="!loading && guideData.nodeConnections">
        <h2>{{ guideData.nodeConnections.title }}</h2>
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
      </section>

      <!-- Node Attributes Section -->
      <section id="node-attributes" v-if="!loading && guideData.nodeAttributes">
        <h2>{{ guideData.nodeAttributes.title }}</h2>
        <h3>{{ guideData.nodeAttributes.overview.title }}</h3>
        <p>{{ guideData.nodeAttributes.overview.content }}</p>

        <!-- Alignment Explanation -->
        <h3>{{ guideData.nodeAttributes.alignmentExplanation.title }}</h3>
        <div v-for="alignment in guideData.nodeAttributes.alignmentExplanation.content" :key="alignment.range">
          <strong>{{ alignment.range }}:</strong> {{ alignment.description }}
        </div>

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
      </section>

      <!-- Export Simulation Data Section -->
      <section id="export-simulation-data" v-if="!loading && exportSimulationData">
        <h2>{{ exportSimulationData.title }}</h2>
        <p>{{ exportSimulationData.content }}</p>
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
          this.fetchExportSimulationData()
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
}

nav ul li {
  margin-bottom: 15px;
}

nav ul li a {
  text-decoration: none;
  color: #007BFF;
  font-weight: bold;
}

nav ul li a:hover,
nav ul li a:focus {
  text-decoration: underline;
}

/* Content area for sections */
.content-area {
  margin-left: 220px;
  padding: 20px;
  flex: 1;
}

html {
  scroll-behavior: smooth;
}

h2, h3, p, table, ol, ul {
  text-align: left;
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  font-size: 24px;
  margin-bottom: 15px;
}

h3 {
  font-size: 20px; /* Adjusted size for better hierarchy */
  margin-bottom: 12px;
}

h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  margin-bottom: 20px;
  max-width: 800px;
  line-height: 1.6;
  word-break: break-word;
  overflow-wrap: break-word;
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
  text-align: left;
  word-break: break-word;
  overflow-wrap: break-word;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
  font-size: 14px; /* Make the text a bit smaller for better readability */
}

td {
  font-size: 14px;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* Adjustments for small screens */
@media screen and (max-width: 768px) {
  .content-area {
    margin-left: 0;
    padding: 10px;
  }

  table {
    font-size: 12px;
    table-layout: auto; /* Allow the table to adapt more dynamically to smaller screens */
  }

  th, td {
    padding: 8px;
  }
}

ol, ul {
  margin-left: 20px;
  margin-bottom: 20px;
  max-width: 800px;
  word-break: break-word;
  overflow-wrap: break-word;
}

.loading {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-top: 50px;
}

/* Add subtle animations for smooth scrolling */
html {
  scroll-behavior: smooth;
}

@media screen and (max-width: 480px) {
  h2 {
    font-size: 22px;
  }

  h3 {
    font-size: 18px;
  }

  p {
    font-size: 14px;
  }

  table {
    font-size: 10px;
  }

  th, td {
    padding: 6px;
  }

  .sticky-sidebar {
    display: none; /* Hide sidebar on small screens */
  }

  .content-area {
    margin-left: 0;
  }
}

@media (min-width: 1201px) {
  .container {
    max-width: 1400px;
  }
}
</style>
