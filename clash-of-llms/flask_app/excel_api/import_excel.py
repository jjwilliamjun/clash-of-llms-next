import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from class_api import gpt_endpoint
from class_api.team import Team
import pandas as pd


def validate_settings(team: dict) -> list:
    '''Checks if imported values for blue and red agents are valid'''

    errors = []

    # TODO: will need to retrieve this list rather than hardcode it
    models = ['gpt-4o-mini', 'gpt-4o', 'gpt-4o-turbo', 'gpt-3.5-turbo', 'custom']
    _model_id = team["Model_ID"].strip()
    _energy = int(team["Energy"])
    _msgs = int(team["Msgs_Generated"])
    _temp = float(team["Temperature"])
    _influence = float(team["Influence_Factor"])
    _max_cost = int(team["Max_Cost"])
    _penalty = int(team["Penalty"])
    _penalty_threshold = int(team["Penalty_Threshold"])

    if _model_id not in models:
        errors.append("invalid model ID for " + team["Team"] + " agent")
    if _energy > 100 or _energy < 1:
        errors.append("invalid energy value: for " + team["Team"] + " agent")
    if _msgs > 10 or _msgs < 1:
        errors.append("invalid msgs value: for " + team["Team"] + " agent")
    if _temp > 1 or _temp < 0:
        errors.append("invalid temp value: for " + team["Team"] + " agent")
    if _influence > 1 or _influence < 0:
        errors.append("invalid influence factor value: for " + team["Team"] + " agent")
    if _max_cost < 0 or _max_cost > 100:
        errors.append("invalid max cost value for " + team["Team"] + " agent")
    if _penalty < 0 or _penalty > 100:
        errors.append("invalid penalty value: for " + team["Team"] + " agent")
    if _penalty_threshold < 0 or _penalty_threshold > 100:
        errors.append("invalid penalty threshold value: for " + team["Team"] + " agent")
    
    return errors


def validate_end_conditions(conditions: dict) -> list:
    '''Checks if imported values for custom termination conditions are valid'''
    errors = []

    _alignment = int(conditions["population_alignment"])
    _rounds = int(conditions["round_number"])

    if _alignment < 0 or _alignment > 100: 
        errors.append("invalid custom termination condition for population alignment. Must be within the range of 0-100 (inclusive)")
    if _rounds < 0 or _rounds > 50: 
        errors.append("invalid custom termination condition for number of rounds. Must be within the range of 0-50 (inclusive)")

    return errors


def import_settings(xls_path) -> tuple:
    '''Returns settings for red and blue teams as dictionaries'''
    settings = pd.read_excel(xls_path)

    red_team = settings.loc[0]
    blue_team = settings.loc[1]
    termination_conditions = {
        "population_alignment" : settings.loc[4]['Model_ID'],
        "round_number" : settings.loc[5]['Model_ID']
    }
    
    red_team = red_team.to_dict()
    blue_team = blue_team.to_dict()

    # To be updated once network files are read
    red_team["Alignment"] = 0
    blue_team["Alignment"] = 0

    input_errors = ["errors"]
    input_errors.extend(validate_settings(red_team))
    input_errors.extend(validate_settings(blue_team))
    input_errors.extend(validate_end_conditions(termination_conditions))

    if len(input_errors) > 1:
        return tuple(input_errors)

    return red_team, blue_team, termination_conditions

def validate_attributes(nodes: dict):
    '''Checks imported attribute values are valid and returns alignments if so.'''

    errors = []
    blue_aligned = 0
    red_aligned = 0
    neutral = 0

    for node in nodes:
        alignment = nodes[node]["Alignment"]
        if alignment > 1 or alignment < -1:
            errors.append("invalid alignment value for " + nodes["Node_ID"])
            return errors
        elif alignment < 1 and alignment > 0.4:
            red_aligned += 1
        elif alignment > -1 and alignment < -0.4:
            blue_aligned += 1
        elif alignment <= 0.4 and alignment <= -0.4:
            neutral += 1
    
    return blue_aligned, red_aligned, neutral, errors

def import_node_attributes(xls_path) -> dict:
    '''Returns node attributes in a dictionary of dictionaries'''
    attributes = pd.read_excel(xls_path)
    nodes = {}
    
    for index, row in attributes.iterrows():
        nodes[row['Node_ID']] = {
            "Alignment": row['Alignment'],
        }

    return nodes

def validate_connections(connections: dict, nodes: dict):
    '''Checks if imported values for node connections are valid'''
    errors = []

    for node in connections:
        connected = connections[node]["Connected_Nodes"].split(", ")
        factors = list(map(float, connections[node]["Influence_Factor"].split(", ")))
        # Check connected nodes are valid nodes
        for c in connected:
            if c not in nodes:
                errors.append("invalid node connection from " + node + " to " + c)
        # Check influence factors are valid
        for f in factors:
            if f > 1 or f < -1:
                errors.append("invalid node connection influence factor: " + str(f) + " for node " + node)
    
    return errors

def import_node_connections(xls_path) -> dict:
    '''Returns node connections in a dictionary of dictionaries'''
    connections = pd.read_excel(xls_path)
    conns = {}

    for index, row in connections.iterrows():
        conns[row['Node']] = {
            "Connected_Nodes": row['Connected_Nodes'],
            "Influence_Factor": row['Influence_Factor']
        }

    return conns
