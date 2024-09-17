<template>
  <div>
    <h2>Network Graph</h2>
    
    <!-- Navigation Controls: Slider and Buttons -->
    <div class="navigation-controls">
      <button @click="navigateRound(-1)" :disabled="selectedRound <= 0">Previous</button>
      <input 
        type="range" 
        v-model="selectedRound" 
        @input="updateGraph(selectedRound)" 
        :min="0" 
        :max="maxRounds" 
        :step="1" 
        class="round-slider"
      />
      <button @click="navigateRound(1)" :disabled="selectedRound >= maxRounds">Next</button>
      <span>Round: {{ selectedRound }}</span>
    </div>
    
    <!-- Graph Container -->
    <div ref="networkGraph" style="width: 100%; height: 600px; border: 1px solid lightgray;"></div>
    
    <!-- Node Details -->
    <div v-if="selectedNode" class="node-details">
      <h3>Node Details</h3>
      <p><strong>ID:</strong> {{ selectedNode.id }}</p>
      <p><strong>Alignment:</strong> {{ selectedNode.Alignment }}</p>
    </div>
    
    <!-- Edge Details -->
    <div v-if="selectedEdge" class="edge-details">
      <h3>Edge Details</h3>
      <p><strong>From:</strong> {{ selectedEdge.from }}</p>
      <p><strong>To:</strong> {{ selectedEdge.to }}</p>
      <p><strong>Influence Factor:</strong> {{ selectedEdge.influence }}</p>
    </div>

    <!-- Display error message if network data is not found -->
    <div v-if="fetchError" class="error-message">
      <p>Error: {{ fetchError }}</p>
    </div>
  </div>
</template>

<script>
import { fetchGraphDataForRound, drawNetworkGraph } from '@/services/graphDataService';

export default {
  data() {
    return {
      selectedNode: null,
      selectedEdge: null,
      selectedRound: 0,
      maxRounds: 10, // Adjust this based on the total number of rounds available
      fetchError: null,
    };
  },
  mounted() {
    this.updateGraph(this.selectedRound);
  },
  methods: {
    async updateGraph(roundNumber) {
      try {
        this.fetchError = null;
        const networkData = await fetchGraphDataForRound(roundNumber);
        this.drawGraph(networkData);
      } catch (error) {
        this.fetchError = `Round ${roundNumber} data not found.`;
      }
    },
    drawGraph(networkData) {
      drawNetworkGraph(
        this.$refs.networkGraph,
        networkData,
        (node) => {
          this.selectedNode = node;
          this.selectedEdge = null;
        },
        (edge) => {
          this.selectedEdge = edge;
          this.selectedNode = null;
        }
      );
    },
    navigateRound(step) {
      // Adjust selectedRound within valid range
      const newRound = this.selectedRound + step;
      if (newRound >= 0 && newRound <= this.maxRounds) {
        this.selectedRound = newRound;
        this.updateGraph(this.selectedRound);
      }
    },
  },
};
</script>

<style scoped>
.navigation-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.round-slider {
  width: 300px; /* Set a fixed width for the slider */
}

.node-details, .edge-details, .error-message {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
