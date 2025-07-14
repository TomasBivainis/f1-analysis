from race_scraper import scrape_race_data
from racetrack_scrapper import scrape_racetrack_data
from weather_scraper import scrape_weather_data
from json_util import *
from race_util import Race

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def count_all_team_points():
  race_results = load_json("race_results.json")
  #race_results = convert_dict_list_to_object_list(race_results, Race)
  
  team_points_per_race = {}
  
  for race_result in race_results:
    team_points_per_race[race_result["city"]] = {}
    
    for result in race_result["race_result"]:
      if result["pos"] == None:
        continue
        #result["pos"] = 20
      
      if result["team"] in team_points_per_race[race_result["city"]]:
        team_points_per_race[race_result["city"]][result["team"]] = (team_points_per_race[race_result["city"]][result["team"]] + result["pos"]) / 2
      else:
        team_points_per_race[race_result["city"]][result["team"]] = result["pos"]
      
  return team_points_per_race

def get_team_points(team, team_points_per_race):
  points = []
  
  for race_result in team_points_per_race.values():
    points.append(race_result[team])
  
  return points

def main():
  team_points_per_race = count_all_team_points()
  weather_data = load_json("weather.json")
  
  data = {
    "team": get_team_points("Mercedes", team_points_per_race),
    "temperature": weather_data.values()
  }
  
  if len(data["team"]) != len(data["temperature"]):
    not_matching_cities = ""
    
    for city in team_points_per_race.keys():
      if city not in weather_data.keys():
        if not_matching_cities == "":
          not_matching_cities = city
        else:
          not_matching_cities = not_matching_cities + ", " + city
    
    raise Exception("Some track cities are not matching: " + not_matching_cities)
  
  df = pd.DataFrame(data)
  
  X = df[['temperature']]  # 2D array
  y = df['team']    # 1D array
  
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model = LinearRegression()
  model.fit(X_train, y_train)
  
  print("Slope:", model.coef_[0])
  print("Intercept:", model.intercept_)
  
  y_pred = model.predict(X_test)

  plt.scatter(X, y, color='blue')             # Original data
  plt.plot(X, model.predict(X), color='red')  # Regression line
  plt.xlabel('Temperature in celsius')
  plt.ylabel('Average team position')
  plt.title('Linear Regression')
  plt.show()
  
  print("MSE:", mean_squared_error(y_test, y_pred))
  print("R^2 Score:", r2_score(y_test, y_pred))
  
if __name__ == "__main__":
  main()