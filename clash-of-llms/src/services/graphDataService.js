import { Network } from 'vis-network/standalone/esm/vis-network';
import { DataSet } from 'vis-data/standalone/esm/vis-data';
import axios from 'axios';

/**
 * Fetches the graph data for a specific round from the backend.
 * @param {number} roundNumber - The round number to fetch the data for.
 * @returns {Promise<Object>} A promise that resolves to the network data for the specified round.
 */
export const fetchGraphDataForRound = async (roundNumber) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/excel_api/round_data/${roundNumber}`);
    if (response.status === 200) {
      return response.data; // Network data for the specified round
    } else {
      throw new Error(`Failed to fetch graph data for round ${roundNumber}.`);
    }
  } catch (error) {
    console.error(`Error fetching graph data for round ${roundNumber}:`, error);
    throw error;
  }
};

/**
 * Interpolates between two colors.
 * @param {string} color1 - The starting color in hex format.
 * @param {string} color2 - The ending color in hex format.
 * @param {number} factor - A factor between 0 and 1 to determine the mix ratio.
 * @returns {string} - The interpolated color in rgb format.
 */
const interpolateColor = (color1, color2, factor) => {
  const result = color1.slice(1).match(/.{1,2}/g)
    .map((hex, i) => {
      return Math.round(
        parseInt(hex, 16) * (1 - factor) + parseInt(color2.slice(1).match(/.{1,2}/g)[i], 16) * factor
      );
    });
  return `rgb(${result.join(',')})`;
};

/**
 * Determines the color for a node based on its alignment value.
 * @param {number} value - The alignment value of the node.
 * @returns {string} - The color of the node.
 */
const getColor = (value) => {
  const normalizedValue = (value + 1) / 2;
  if (normalizedValue <= 0.25) {
    return interpolateColor('#FF0000', '#FF7F7F', normalizedValue / 0.25);
  } else if (normalizedValue > 0.5 && normalizedValue <= 0.75) {
    return interpolateColor('#31a354', '#0e86d4', (normalizedValue - 0.5) / 0.25);
  } else if (normalizedValue > 0.75 && normalizedValue <= 1) {
    return interpolateColor('#0e86d4', '#0006b1', (normalizedValue - 0.75) / 0.25);
  } else {
    return '#0006b1';
  }
};

/**
 * Draws the network graph on a given container element.
 * @param {HTMLElement} container - The DOM element to render the network graph in.
 * @param {Object} networkData - The network data to visualize.
 * @param {Function} [nodeClickHandler] - Optional callback for node click events.
 * @param {Function} [edgeClickHandler] - Optional callback for edge click events.
 */
export const drawNetworkGraph = (container, networkData, nodeClickHandler, edgeClickHandler) => {
  const data = {
    nodes: new DataSet(
      networkData.nodes.map(node => {
        const color = getColor(node.Alignment);
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
        title: `Influence Factor: ${link.weight}`,
        color: {
          color: 'green',
        },
        width: 2,
        influence: link.weight,
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

  // Handle node and edge events if callbacks are provided
  if (nodeClickHandler) {
    network.on('doubleClick', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = networkData.nodes.find(n => n.id === nodeId);
        nodeClickHandler(node);
      }
    });
  }

  if (edgeClickHandler) {
    network.on('selectEdge', (params) => {
      if (params.edges.length > 0) {
        const edgeId = params.edges[0];
        const edge = data.edges.get(edgeId);
        edgeClickHandler(edge);
      }
    });
  }
};
