<template>
  <div>
    <h2>Network Graph</h2>
    <div ref="networkGraph" style="width: 100%; height: 600px; border: 1px solid lightgray;"></div>
    <div v-if="selectedNode" class="node-details">
      <h3>Node Details</h3>
      <p><strong>ID:</strong> {{ selectedNode.id }}</p>
      <p><strong>Alignment:</strong> {{ selectedNode.Alignment }}</p>
    </div>
    <div v-if="selectedEdge" class="edge-details">
      <h3>Edge Details</h3>
      <p><strong>From:</strong> {{ selectedEdge.from }}</p>
      <p><strong>To:</strong> {{ selectedEdge.to }}</p>
      <p><strong>Influence Factor:</strong> {{ selectedEdge.influence }}</p>
    </div>
  </div>
</template>

<script>
import { Network } from 'vis-network/standalone/esm/vis-network';
import { DataSet } from 'vis-data/standalone/esm/vis-data';

export default {
  data() {
    return {
      selectedNode: null, // To store the currently selected node's details
      selectedEdge: null, // To store the currently selected edge's details
      networkData: null,  // To store the network data
    };
  },
  mounted() {
    this.checkForNetworkData();
  },
  methods: {
    async checkForNetworkData() {
      const pollInterval = 2000; // Check every 2 seconds
      const poll = setInterval(async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/network_output.json');
          if (response.ok) {
            const networkData = await response.json();
            this.networkData = networkData;
            this.drawNetwork(networkData);
            clearInterval(poll); // Stop polling once the data is loaded
          }
        } catch (error) {
          console.error('Error loading network data:', error);
        }
      }, pollInterval);
    },
    drawNetwork(networkData) {
      const container = this.$refs.networkGraph;

      // Helper function to interpolate between two colors
      function interpolateColor(color1, color2, factor) {
        const result = color1.slice(1).match(/.{1,2}/g)
          .map((hex, i) => {
            return Math.round(
              parseInt(hex, 16) * (1 - factor) + parseInt(color2.slice(1).match(/.{1,2}/g)[i], 16) * factor
            );
          });
        return `rgb(${result.join(',')})`;
      }

      // Function to determine color based on alignment using predefined color levels
      function getColor(value) {
        // Convert value from [-1, 1] to [0, 1] for interpolation
        const normalizedValue = (value + 1) / 2;

        // Define color stops
        if (normalizedValue <= 0.25) {
          // Interpolate between Red and Light Red
          return interpolateColor('#FF0000', '#FF7F7F', normalizedValue / 0.25);
        } else if (normalizedValue > 0.5 && normalizedValue <= 0.75) {
          // Interpolate between Green and Greenish Blue
          return interpolateColor('#31a354', '#0e86d4', (normalizedValue - 0.5) / 0.25);
        } else if (normalizedValue > 0.75 && normalizedValue <= 1) {
          // Interpolate between Greenish Blue and Deep Blue
          return interpolateColor('#0e86d4', '#0006b1', (normalizedValue - 0.75) / 0.25);
        } else {
          return '#0006b1'; // Fallback to Deep Blue
        }
      }

      const data = {
        nodes: new DataSet(
          networkData.nodes.map(node => {
            const color = getColor(node.Alignment); // Use the color interpolation function
            return {
              id: node.id,
              label: node.id,
              title: `${node.id}: Alignment: ${node.Alignment}`,
              color: {
                background: color,
                border: 'darkgreen',
              },
              font: {
                color: 'white',
              },
              shape: 'circle',
            };
          })
        ),
        edges: new DataSet(
          networkData.links.map(link => ({
            from: link.source,
            to: link.target,
            title: `Influence Factor: ${link.weight}`,  // Display influence factor when hovering over the edge
            color: {
              color: 'green',
            },
            width: 2,
            influence: link.weight,  // Store the influence factor for later use
          }))
        ),
      };

      const options = {
        layout: {
          randomSeed: 42,
          improvedLayout: true,
          hierarchical: false,
        },
        interaction: {
          dragNodes: true,
          zoomView: true,
          dragView: true,
        },
        physics: {
          enabled: true,
          forceAtlas2Based: {
            gravitationalConstant: -50,
            centralGravity: 0.005,
            springLength: 100,
            springConstant: 0.08,
            damping: 0.4,
            avoidOverlap: 0.5,
          },
          solver: 'forceAtlas2Based',
          stabilization: {
            enabled: true,
            iterations: 2000,
            updateInterval: 25,
          },
        },
        autoResize: true,
        height: '100%',
        width: '100%',
      };

      const network = new Network(container, data, options);

      // Disable physics after stabilization
      network.once('stabilizationIterationsDone', () => {
        network.setOptions({ physics: false });
      });

      network.on('doubleClick', (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          this.selectedNode = networkData.nodes.find(node => node.id === nodeId);
          this.selectedEdge = null; // Clear edge selection when a node is selected
        }
      });

      network.on('selectEdge', (params) => {
        if (params.edges.length > 0) {
          const edgeId = params.edges[0];
          const edge = data.edges.get(edgeId);
          this.selectedEdge = {
            from: edge.from,
            to: edge.to,
            influence: edge.influence
          };
          this.selectedNode = null; // Clear node selection when an edge is selected
        }
      });
    },
  },
};
</script>


<style scoped>
.node-details, .edge-details {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>