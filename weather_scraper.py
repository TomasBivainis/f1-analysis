from json_util import *

def get_race_weather():
  racetracks = load_json("racetracks")
  race_results = load_json("race_results")
  
  print(racetracks)
  print(race_results)


if __name__ == "__main__":
  get_race_weather()