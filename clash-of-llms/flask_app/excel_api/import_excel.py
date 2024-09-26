import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from class_api import gpt_endpoint
from class_api.team import Team
import pandas as pd


def validate_settings(team: dict) -> list:

    errors = []

    models = ['gpt-4o-mini', 'gpt-4o', 'gpt-4o-turbo', 'gpt-3.5-turbo', 'custom']
    _energy = int(team["Energy"])
    _msgs = int(team["Msgs_Generated"])
    _temp = float(team["Temperature"])
    _influence = float(team["Influence_Factor"])
    _alignment = float(team["Alignment"])
    _max_cost = int(team["Max_Cost"])

    if team["Model_ID"] not in models:
        errors.append("invalid model ID for " + team["Team"] + " agent")
    if _energy > 100 or _energy < 1:
        errors.append("invalid energy value: for " + team["Team"] + " agent")
    if _msgs > 10 or _msgs < 1:
        errors.append("invalid msgs value: for " + team["Team"] + " agent")
    if _temp > 1 or _temp < 0:
        errors.append("invalid temp value: for " + team["Team"] + " agent")
    if _influence > 1 or _influence < 0:
        errors.append("invalid influence factor value: for " + team["Team"] + " agent")
    if _alignment > 100 or _alignment < 0:
        errors.append("invalid alignment value: for " + team["Team"] + " agent")
    if _max_cost < 0 or _max_cost > 100:
        errors.append("invalid max cost value: for " + team["Team"] + " agent")
    
    return errors


# Returns settings for red and blue teams as dictionaries
def import_settings(xls_path) -> tuple:
    settings = pd.read_excel(xls_path)

    red_team = settings.loc[0]
    blue_team = settings.loc[1]

    red_team = red_team.to_dict()
    blue_team = blue_team.to_dict()

    input_errors = ["errors"]
    input_errors.extend(validate_settings(red_team))
    input_errors.extend(validate_settings(blue_team))

    if len(input_errors) > 1:
        return tuple(input_errors)

    return red_team, blue_team


# Returns node attributes in a dictionary of dictionaries
def import_node_attributes(xls_path) -> dict:
    attributes = pd.read_excel(xls_path)
    nodes = {}
    
    for index, row in attributes.iterrows():
        nodes[row['Node_ID']] = {
            "Alignment": row['Alignment'],
        }

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

    return conns
