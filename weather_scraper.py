from json_util import *
from race_util import Race, Racetrack
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_racetrack_information():
  racetracks = convert_dict_list_to_object_list(load_json("racetracks.json"), Racetrack)
  race_results = convert_dict_list_to_object_list(load_json("race_results.json"), Race)
  
  completed_race_coordinates = {}
  
  for race in race_results:
    for racetrack in racetracks:
      if race.city == racetrack.city:
        completed_race_coordinates[race.city] = [racetrack.latitude, racetrack.longitude, race.date_end]
  
  return completed_race_coordinates

def get_race_day_average_temperature(latitude: int, longitude: int, date: str):
  url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    f"&timezone=America%2FNew_York"
  )
  
  response = requests.get(url)
  data = response.json()
  
  max_temperature = data["daily"]["temperature_2m_max"][0]
  min_temperature = data["daily"]["temperature_2m_min"][0]

  return (max_temperature + min_temperature) / 2

def get_weather_data():
  print("Gathering weather data...")
  
  completed_race_coordinates = get_racetrack_information()
  
  race_weather = {}
  
  for city, [latitude, longitude, date] in completed_race_coordinates.items():
    print(city)
    race_weather[city] = get_race_day_average_temperature(latitude, longitude, date)
  
  save_to_json(race_weather, "weather")
  
  print("Gathering complete!")

if __name__ == "__main__":
  get_weather_data()