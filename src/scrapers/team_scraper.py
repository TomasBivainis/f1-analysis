from src.utils.json_util import *

def get_all_teams():
  race_result = load_json("race_results.json")[0]["race_result"]
  
  teams = []
  
  for driver in race_result:
    if driver["team"] not in teams:
      teams.append(driver["team"])
  
  return teams
  
  