import networkx as nx
from import_settings import import_settings, import_node_attributes, import_node_connections

def create_node_network(attributes_file_path, connections_file_path):
    """
    Creates a node network based on attributes and connections provided in the 
    specified Excel files.
    """
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

# Example usage
if __name__ == '__main__':
    ATTRIBUTES_FILE_PATH = 'NodeAttributes.xlsx'
    CONNECTIONS_FILE_PATH = 'NodeConnections.xlsx'

    network_graph = create_node_network(ATTRIBUTES_FILE_PATH, CONNECTIONS_FILE_PATH)

    print("Nodes:", network_graph.nodes(data=True))
    print("Edges:", network_graph.edges(data=True))
