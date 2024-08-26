<template>
  <div>
    <h2>Network Graph</h2>
    <div ref="networkGraph" style="width: 100%; height: 600px; border: 1px solid lightgray;"></div>
    <div v-if="selectedNode" class="node-details">
      <h3>Node Details</h3>
      <p><strong>ID:</strong> {{ selectedNode.id }}</p>
      <p><strong>Alignment:</strong> {{ selectedNode.Alignment }}</p>
      <p><strong>Uncertainty:</strong> {{ selectedNode.Uncertainty }}</p>
      <p><strong>Influence Potential:</strong> {{ selectedNode.Influence_Potential }}</p>
    </div>
  </div>
</template>

<script>
import { Network } from 'vis-network/standalone/esm/vis-network';
import { DataSet } from 'vis-data/standalone/esm/vis-data';
import networkData from '../../excel_api/network_output.json'; // Adjust the path if necessary

export default {
  data() {
    return {
      selectedNode: null, // To store the currently selected node's details
    };
  },
  mounted() {
    this.loadNetworkData();
  },
  methods: {
    loadNetworkData() {
      console.log('Loading static network data...');
      this.drawNetwork(networkData);
    },
    drawNetwork(networkData) {
      const container = this.$refs.networkGraph;

      const data = {
        nodes: new DataSet(
          networkData.nodes.map(node => {
            let color;
            if (node.Alignment > 0.5) {
              color = 'red';
            } else if (node.Alignment < -0.5) {
              color = 'blue';
            } else {
              color = 'green';
            }
            return {
              id: node.id,
              label: node.id,
              title: `Alignment: ${node.Alignment}\nUncertainty: ${node.Uncertainty}\nInfluence Potential: ${node.Influence_Potential}`,
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
            color: {
              color: 'green', // Customize the color to match the nodes
            },
            width: 2, // Customize the width of the edges
          }))
        ),
      };

      console.log('Rendering network with data:', data);  // Log the data used for rendering

      const options = {
        layout: {
          randomSeed: 42, // Use a fixed random seed for reproducibility
          improvedLayout: true, // Use improved layout for better visualization
          hierarchical: false, // Disable hierarchical layout for more balanced layout
        },
        interaction: {
          dragNodes: true, // Enable dragging of nodes
          zoomView: true,  // Enable zooming
          dragView: true,  // Enable dragging of the entire view
          navigationButtons: false, // Remove navigation buttons
        },
        physics: {
          enabled: true, // Enable physics for more natural layout
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

      // Listen for double-click events on the nodes
      network.on('doubleClick', (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          this.selectedNode = networkData.nodes.find(node => node.id === nodeId);
        }
      });
    },
  },
};
</script>

<style scoped>
.node-details {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
