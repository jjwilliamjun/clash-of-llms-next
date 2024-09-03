import networkx as nx
import json
import os
from create_node_network.green_team import GreenTeam
from import_excel import import_node_attributes, import_node_connections

def create_node_network(node_attributes, node_connections):

    graph = nx.DiGraph()

    # Add nodes with their attributes
    for node_id, attributes in node_attributes.items():
        graph.add_node(node_id, **attributes)

    # Add edges (connections between nodes) with weights
    for node_id, connection in node_connections.items():
        connected_nodes = connection['Connected_Nodes'].split(',')
        influence_factors = map(float, connection['Influence_Factor'].split(','))

        for target_node, influence in zip(connected_nodes, influence_factors):
            graph.add_edge(node_id, target_node.strip(), weight=influence)
#Initialises green team. TODO: pass in num. of nodes aligned towards red, and towards blue 
#Currently hard codes them to 30 and 20
    GreenTeam(graph, 30, 20) 
    # Convert the graph to node-link data format, which is suitable for saving as JSON
    graph_data = nx.node_link_data(graph)

    # Define the correct path for saving the JSON file
    json_path = os.path.join(os.getcwd(), 'excel_api', 'create_node_network', 'network_output.json')
    
    # Print the current working directory and the full path to the JSON file
    print(f"Saving network to: {json_path}")

    # Save the graph data as a JSON file
    try:
        with open(json_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"Network JSON file successfully created at: {json_path}")
    except Exception as e:
        print(f"Failed to save network JSON file: {str(e)}")

# Example usage
if __name__ == '__main__':
    # Assuming that the import_excel.py script provides the following functions


    # Load node attributes and connections from Excel files
    node_attributes = import_node_attributes('./create_node_network/NodeAttributes.xlsx')
    node_connections = import_node_connections('./create_node_network/NodeConnections.xlsx')

    # Create the network and save it as network_output.json
    create_node_network(node_attributes, node_connections)
