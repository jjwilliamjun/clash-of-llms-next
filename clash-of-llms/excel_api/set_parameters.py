import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from class_api.team import team

# Given a dict, creates and returns a team object
def set_team(team_parameters: dict) -> team:

    team_parameters["Model_ID"] = team_parameters["Model_ID"].strip()
    team_parameters["Energy"] = int(team_parameters["Energy"])
    team_parameters["Msgs_Generated"] = int(team_parameters["Msgs_Generated"])
    team_parameters["Temperature"] = float(team_parameters["Temperature"])
    team_parameters["Influence_Factor"] = float(team_parameters["Influence_Factor"])
    
    new_team = team(
        team=team_parameters["Team"], 
        model_ID=team_parameters["Model_ID"],
        energy=team_parameters["Energy"],
        potency=0,
        msg_count=team_parameters["Msgs_Generated"],
        influence_factor=team_parameters["Influence_Factor"],
        alignment=5,
        max_cost=5,
        temperature=team_parameters["Temperature"]
    )

    return new_team
