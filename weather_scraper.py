from json_util import *
from race_util import Race, Racetrack

def get_race_weather():
  racetracks = convert_dict_list_to_object_list(load_json("racetracks.json"), Racetrack)
  race_results = convert_dict_list_to_object_list(load_json("race_results.json"), Race)
  
  completed_race_coordinates = {}
  
  for race in race_results:
    for racetrack in racetracks:
      if race.city == racetrack.city:
        completed_race_coordinates[race.city] = [racetrack.latitude, racetrack.longitude, race.date_end]
  
  print(completed_race_coordinates)


if __name__ == "__main__":
  get_race_weather()