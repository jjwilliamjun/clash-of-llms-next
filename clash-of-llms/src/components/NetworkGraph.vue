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

export default {
  data() {
    return {
      selectedNode: null, // To store the currently selected node's details
      networkData: null, // To store the network data
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
              color: 'green',
            },
            width: 2,
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
