import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from class_api.team import Team, BlueTeam, RedTeam

# Given a dict, creates and returns a team object
def set_team(team_parameters: dict) -> Team:

    # Strip any extra spaces from the model ID
    team_parameters["Model_ID"] = team_parameters["Model_ID"].strip()
    
    # Convert parameters to the appropriate data types
    team_parameters["Energy"] = int(team_parameters["Energy"])
    team_parameters["Msgs_Generated"] = int(team_parameters["Msgs_Generated"])
    team_parameters["Temperature"] = float(team_parameters["Temperature"])
    team_parameters["Influence_Factor"] = float(team_parameters["Influence_Factor"])
    team_parameters["Alignment"] = float(team_parameters["Alignment"])
    team_parameters["Max_Cost"] = float(team_parameters["Max_Cost"])
    team_parameters["Penalty"] = float(team_parameters["Penalty"])
    team_parameters["Penalty_Threshold"] = float(team_parameters["Penalty_Threshold"])

    if team_parameters["Team"].lower() == "blue":
        # Initialize and return the new red team object
        new_team = BlueTeam(
            team=team_parameters["Team"], 
            model_ID=team_parameters["Model_ID"],
            energy=team_parameters["Energy"],
            potency=0,
            msg_count=team_parameters["Msgs_Generated"],
            influence_factor=team_parameters["Influence_Factor"],
            alignment=team_parameters["Alignment"],
            max_cost=team_parameters["Max_Cost"],
            temperature=team_parameters["Temperature"]
        )
        
        return new_team
    
    else:    
        # Initialize and return the new blue team object
        new_team = RedTeam(
            team=team_parameters["Team"], 
            model_ID=team_parameters["Model_ID"],
            potency=0,
            msg_count=team_parameters["Msgs_Generated"],
            influence_factor=team_parameters["Influence_Factor"],
            alignment=team_parameters["Alignment"],
            temperature=team_parameters["Temperature"],
            penalty=team_parameters["Penalty"],
            penalty_threshold=team_parameters["Penalty_Threshold"]
        )

        return new_team
