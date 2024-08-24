import networkx as nx
import matplotlib.pyplot as plt
from import_settings import import_node_attributes, import_node_connections

def create_node_network(attributes_file_path, connections_file_path):
    # Import node attributes and connections using the functions you defined
    node_attributes = import_node_attributes(attributes_file_path)
    node_connections = import_node_connections(connections_file_path)

    # Initialize a new graph
    graph = nx.Graph()

    # Add nodes with attributes
    for node_id, attributes in node_attributes.items():
        graph.add_node(node_id, **attributes)

    # Add edges based on connections
    for node_id, connection in node_connections.items():
        connected_nodes = connection['Connected_Nodes'].split(',')
        influence_factors = map(float, connection['Influence_Factor'].split(','))

        for target_node, influence in zip(connected_nodes, influence_factors):
            graph.add_edge(node_id, target_node.strip(), weight=influence)

    return graph

def visualize_graph(graph):
    pos = nx.spring_layout(graph)

    # Create node labels with alignment values, using a default if missing
    node_labels = {}
    for node, data in graph.nodes(data=True):
        alignment = data.get('Alignment', 0.0)  # Use 0.0 if 'Alignment' is missing
        node_labels[node] = f"{node}\nAlign: {alignment:.2f}"
    
    nx.draw(graph, pos, labels=node_labels, node_color="lightblue", node_size=500, font_size=10)
    
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.show()

# Example usage
if __name__ == '__main__':
    attributes_file_path = 'NodeAttributes.xlsx'  # Path to your node attributes file
    connections_file_path = 'NodeConnections.xlsx'  # Path to your node connections file

    try:
        graph = create_node_network(attributes_file_path, connections_file_path)

        # Print nodes and their attributes
        print("Nodes:")
        for node, attr in graph.nodes(data=True):
            print(f"{node}: {attr}")

        # Print edges and their attributes
        print("\nEdges:")
        for edge in graph.edges(data=True):
            print(edge)

        # Visualize the graph
        visualize_graph(graph)

    except Exception as e:
        print(f"An error occurred: {e}")
