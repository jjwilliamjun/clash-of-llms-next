<template>
  <div class="about">
    <!-- Introduction Section -->
    <section v-if="introduction">
      <h2>{{ introduction.title }}</h2>
      <p>{{ introduction.content }}</p>
    </section>

    <!-- Node Connections Section -->
    <section v-if="nodeConnections">
      <h2>{{ nodeConnections.title }}</h2>
      <h3>{{ nodeConnections.overview.title }}</h3>
      <p>{{ nodeConnections.overview.content }}</p>

      <!-- Node Connections Structure Table -->
      <h3>{{ nodeConnections.structure.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in nodeConnections.structure.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in nodeConnections.structure.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Node Connections Example Table -->
      <h3>{{ nodeConnections.example.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in nodeConnections.example.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in nodeConnections.example.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Instructions -->
      <h3>{{ nodeConnections.instructions.title }}</h3>
      <ol>
        <li v-for="instruction in nodeConnections.instructions.content" :key="instruction">{{ instruction }}</li>
      </ol>

      <!-- Tips -->
      <h3>{{ nodeConnections.tips.title }}</h3>
      <ul>
        <li v-for="tip in nodeConnections.tips.content" :key="tip">{{ tip }}</li>
      </ul>

      <!-- Download link for NodeConnections.xlsx -->
      <p>
        <strong>Download Example File: </strong>
        <a href="/documents/NodeConnections.xlsx" download>NodeConnections.xlsx</a>
      </p>
    </section>

    <!-- Node Attributes Section -->
    <section v-if="nodeAttributes">
      <h2>{{ nodeAttributes.title }}</h2>
      <h3>{{ nodeAttributes.overview.title }}</h3>
      <p>{{ nodeAttributes.overview.content }}</p>

      <!-- Node Attributes Structure Table -->
      <h3>{{ nodeAttributes.structure.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in nodeAttributes.structure.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in nodeAttributes.structure.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Alignment Explanation Section (2.3) -->
      <h3>{{ nodeAttributes.alignmentExplanation.title }}</h3>
      <p>
        The <strong>Alignment</strong> value indicates the initial stance of the node:
      </p>
      <ul>
        <li v-for="(item, index) in nodeAttributes.alignmentExplanation.content" :key="index">
          <strong>{{ item.range }}</strong>: {{ item.description }}
        </li>
      </ul>


      <!-- Node Attributes Example Table -->
      <h3>{{ nodeAttributes.example.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in nodeAttributes.example.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in nodeAttributes.example.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Instructions -->
      <h3>{{ nodeAttributes.instructions.title }}</h3>
      <ol>
        <li v-for="instruction in nodeAttributes.instructions.content" :key="instruction">{{ instruction }}</li>
      </ol>

      <!-- Tips -->
      <h3>{{ nodeAttributes.tips.title }}</h3>
      <ul>
        <li v-for="tip in nodeAttributes.tips.content" :key="tip">{{ tip }}</li>
      </ul>

      <!-- Download link for NodeAttributes.xlsx -->
      <p>
        <strong>Download Example File: </strong>
        <a href="/documents/NodeAttributes.xlsx" download>NodeAttributes.xlsx</a>
      </p>
    </section>

    <!-- Simulation Settings Section -->
    <section v-if="simulationSettings">
      <h2>{{ simulationSettings.title }}</h2>
      <h3>{{ simulationSettings.overview.title }}</h3>
      <p>{{ simulationSettings.overview.content }}</p>

      <!-- Simulation Settings Structure Table -->
      <h3>{{ simulationSettings.structure.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in simulationSettings.structure.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in simulationSettings.structure.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Simulation Settings Example Table -->
      <h3>{{ simulationSettings.example.title }}</h3>
      <table>
        <thead>
          <tr>
            <th v-for="header in simulationSettings.example.tableHeaders" :key="header">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in simulationSettings.example.tableContent" :key="row[0]">
            <td v-for="cell in row" :key="cell">{{ cell }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Instructions -->
      <h3>{{ simulationSettings.instructions.title }}</h3>
      <ol>
        <li v-for="instruction in simulationSettings.instructions.content" :key="instruction">{{ instruction }}</li>
      </ol>

      <!-- Download link for SimulationSetting.xlsx -->
      <p>
        <strong>Download Example File: </strong>
        <a href="/documents/SimulationSetting.xlsx" download>SimulationSetting.xlsx</a>
      </p>
    </section>

    <!-- Importing Files Section -->
    <section v-if="importingFiles">
      <h2>{{ importingFiles.title }}</h2>
      <ol>
        <li v-for="step in importingFiles.steps" :key="step">{{ step }}</li>
      </ol>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      introduction: null,
      nodeConnections: null,
      nodeAttributes: null,
      simulationSettings: null,
      importingFiles: null
    };
  },
  mounted() {
    this.fetchGuideData();
  },
  methods: {
    async fetchGuideData() {
      try {
        const response = await axios.get('/documents/guide.json'); // Fetch the JSON file
        const data = response.data;
        this.introduction = data.introduction;
        this.nodeConnections = data.nodeConnections;
        this.nodeAttributes = data.nodeAttributes;
        this.simulationSettings = data.simulationSettings;
        this.importingFiles = data.importingFiles;
      } catch (error) {
        console.error('Error fetching guide data:', error);
      }
    }
  }
};
</script>

<style scoped>
.about {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
  line-height: 1.6;
  font-family: Arial, sans-serif;
}

section {
  margin-bottom: 40px;
}

/* Left-align all headers and content */
h2, h3, p, ol, ul, table {
  text-align: left;
}

/* Style for the headers */
h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  text-align: left;
}

h3 {
  font-size: 20px;
  color: #444;
  margin-bottom: 15px;
  text-align: left;
}

p {
  font-size: 16px;
  margin-bottom: 20px;
  text-align: left;
}

/* Table Styling */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 2px solid black;
  text-align: left;
}

th, td {
  border: 2px solid black;
  padding: 10px;
  text-align: left;
  vertical-align: middle;
}

th {
  background-color: #f7f7f7;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* List Styling */
ol, ul {
  padding-left: 20px;
  margin-bottom: 20px;
}

</style>
