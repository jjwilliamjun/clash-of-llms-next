import pandas as pd

# Returns settings for red and blue teams as dictionaries
def import_settings(xls_path) -> tuple:
    settings = pd.read_excel(xls_path)

    red_team = settings.loc[0]
    blue_team = settings.loc[1]

    red_team.to_dict()
    blue_team.to_dict()

    # TO DO --> return objects for red/blue teams
    # TO DO --> validate input?

    return red_team, blue_team


# Returns node attribues in a dictionary of dictionaries
def import_node_attributes(xls_path) -> dict:
    attributes = pd.read_excel(xls_path)
    nodes = {}
    
    for index, row in attributes.iterrows():
        nodes[row['Node_ID']] = {
            "Alignment": row['Alignment'],
            "Uncertainty": row['Uncertainty'],
            "Influence_Potential": row['Influence_Potential']
        }
    
    # TO DO --> modify to store nodes appropriately

    return nodes


# Returns node connections in a dictionary of dictionaries
def import_node_connections(xls_path) -> dict:
    connections = pd.read_excel(xls_path)
    conns = {}

    for index, row in connections.iterrows():
        conns[row['Node']] = {
            "Connected_Nodes": row['Connected_Nodes'],
            "Influence_Factor": row['Influence_Factor']
        }

    # TO DO --> modify to store connections appropriately

    return conns