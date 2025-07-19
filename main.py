from race_scraper import scrape_race_data
from racetrack_scrapper import scrape_racetrack_data
from weather_scraper import scrape_weather_data, get_only_needed_weather_data
from json_util import *
from race_util import Race
from team_scraper import get_all_teams

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.widgets import Button
from matplotlib.ticker import MultipleLocator

def count_all_team_points():
  race_results = load_json("race_results.json")
  #race_results = convert_dict_list_to_object_list(race_results, Race)
  
  team_points_per_race = {}
  
  # if both drivers finish: average
  # if one driver finishes: his position
  # if none: 20
  
  for race_result in race_results:
    team_points_per_race[race_result["city"]] = {}
    
    one_driver_out = []
    
    for result in race_result["race_result"]:
      if result["pos"] == None:
        if result["team"] in one_driver_out:
          team_points_per_race[race_result["city"]][result["team"]] = 21
        else:
          one_driver_out.append(result["team"])
        continue
      
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
  teams = get_all_teams()
  
  
  target = "Temperature"
  
  dfs = {}
  
  for team in teams:
    data = {}
    temp_points = get_team_points(team, team_points_per_race)
    temp_weather = get_only_needed_weather_data(temp_points, list(weather_data.values()))
    
    for i in reversed(range(len(temp_points))):
      if temp_points[i] == 21:
        temp_points.pop(i)
    
    data["points"] = temp_points
    data[target] = temp_weather
    dfs[team] = pd.DataFrame(data)
  
  current_index = [0]
  
  fig, ax = plt.subplots()
  plt.subplots_adjust(bottom=0.2)
  
  def plot_regression(team_index):
    ax.clear()
    df = dfs[teams[team_index]]
    
    X = df[[target]].values
    y = df["points"].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    ax.scatter(X, y, label='Actual')
    ax.plot(X, y_pred, color='red', label='Regression line')
    ax.set_title(f'{teams[team_index]} vs {target}')
    ax.set_xlabel(target)
    ax.set_ylabel(teams[team_index])
    ax.set_ylim(0.5, 20.5)
    ax.yaxis.set_major_locator(MultipleLocator(2)) 
    ax.legend()
    fig.canvas.draw_idle()
  
  # Button callbacks
  def next_plot(event):
      current_index[0] = (current_index[0] + 1) % len(teams)
      plot_regression(current_index[0])
  
  def prev_plot(event):
    current_index[0] = (current_index[0] - 1) % len(teams)
    plot_regression(current_index[0])
  
  # Buttons
  axprev = plt.axes([0.2, 0.05, 0.1, 0.075])
  axnext = plt.axes([0.7, 0.05, 0.1, 0.075])
  bnext = Button(axnext, 'Next →')
  bprev = Button(axprev, '← Prev')
  bnext.on_clicked(next_plot)
  bprev.on_clicked(prev_plot)

  # Initial plot
  plot_regression(current_index[0])
  plt.show()
  
  
  
if __name__ == "__main__":
  main()