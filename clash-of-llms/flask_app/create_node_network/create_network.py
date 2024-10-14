import math
import networkx as nx
import json
import random
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...')))


green_team = None

def generate_random_network(node_count):
    node_attributes = {}
    node_connections = {}

    for i in range(1, node_count + 1):
        node_id = f'Node_{i}'
        alignment = round(random.uniform(-1, 1), 2)
        
        node_attributes[node_id] = {
            "Alignment": alignment,
            "id": node_id,
            "rejectMessaging": False, #Default is false 
        }
        
        # Generate random directed connections for each node
        connected_nodes = random.sample(range(1, node_count + 1), random.randint(1, 5))
        connected_nodes = [f'Node_{n}' for n in connected_nodes if n != i]  # Exclude self-loops
        influence_factors = [round(random.uniform(0.2, 0.5), 2) for _ in connected_nodes]
        
        node_connections[node_id] = {
            "Connected_Nodes": ",".join(connected_nodes),
            "Influence_Factor": ",".join(map(str, influence_factors))
        }
        
        # Optionally, add reciprocal connections
        for target_node in connected_nodes:
            if target_node not in node_connections:
                reverse_influence = round(random.uniform(0.2, 0.5), 2)
                node_connections[target_node] = {
                    "Connected_Nodes": node_id,
                    "Influence_Factor": str(reverse_influence)
                }
            else:
                node_connections[target_node]["Connected_Nodes"] += f",{node_id}"
                reverse_influence = round(random.uniform(0.2, 0.5), 2)
                node_connections[target_node]["Influence_Factor"] += f",{reverse_influence}"

    return node_attributes, node_connections

def generate_user_input_network(node_count, connections_per_node):
    node_attributes = {}
    node_connections = {}

    for i in range(1, node_count + 1):
        node_id = f'Node_{i}'
        alignment = round(random.uniform(-1, 1), 2)
        
        node_attributes[node_id] = {
            "Alignment": alignment,
            "id": node_id,
            "rejectMessaging": False, #Default is false 
        }
        
        # Use user-defined connections for each node
        connected_nodes = random.sample(range(1, node_count + 1), connections_per_node)
        connected_nodes = [f'Node_{n}' for n in connected_nodes if n != i]  # Exclude self-loops
        influence_factors = [round(random.uniform(0.2, 0.5), 2) for _ in connected_nodes]
        
        node_connections[node_id] = {
            "Connected_Nodes": ",".join(connected_nodes),
            "Influence_Factor": ",".join(map(str, influence_factors))
        }
        
        # Optionally, add reciprocal connections
        for target_node in connected_nodes:
            if target_node not in node_connections:
                reverse_influence = round(random.uniform(0.2, 0.5), 2)
                node_connections[target_node] = {
                    "Connected_Nodes": node_id,
                    "Influence_Factor": str(reverse_influence)
                }
            else:
                node_connections[target_node]["Connected_Nodes"] += f",{node_id}"
                reverse_influence = round(random.uniform(0.2, 0.5), 2)
                node_connections[target_node]["Influence_Factor"] += f",{reverse_influence}"

    return node_attributes, node_connections

def create_node_network(node_attributes, node_connections):
    graph = nx.DiGraph()  # Create a directed graph
    global green_team
    
    # Add nodes with their attributes
    for node_id, attributes in node_attributes.items():
        graph.add_node(node_id, **attributes)
        
    # Ensure all nodes have the `rejectMessaging` attribute
    for node_id in graph.nodes:
        if 'rejectMessaging' not in graph.nodes[node_id]:
            graph.nodes[node_id]['rejectMessaging'] = False
    # Add edges (connections between nodes) with weights
    for node_id, connection in node_connections.items():
        connected_nodes = connection['Connected_Nodes'].split(',')
        influence_factors = map(float, connection['Influence_Factor'].split(','))

        for target_node, influence in zip(connected_nodes, influence_factors):
            graph.add_edge(node_id, target_node.strip(), weight=round(influence, 2))

    # Convert the graph to node-link data format, which is suitable for saving as JSON
    graph_data = nx.node_link_data(graph)

    # Create round_data directory if it doesn't exist
    dir_path = os.path.join(os.getcwd(), 'flask_app', 'create_node_network', 'round_data')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Save the graph data as `round_0.json`
    json_path = os.path.join(os.getcwd(), 'flask_app', 'create_node_network', 'round_data', 'round_0.json')
    print(f"Saving network to: {json_path}")

    # Save the graph data as a JSON file
    try:
        with open(json_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"Initial network JSON file successfully created at: {json_path}")
    except Exception as e:
        print(f"Failed to save initial network JSON file: {str(e)}")
    return graph

# Example usage
if __name__ == '__main__':
    # Assuming that the import_excel.py script provides the following functions


    # Load node attributes and connections from Excel files
    node_attributes = import_node_attributes('./create_node_network/NodeAttributes.xlsx')
    node_connections = import_node_connections('./create_node_network/NodeConnections.xlsx')

    # Create the network and save it as network_output.json
    create_node_network(node_attributes, node_connections)


