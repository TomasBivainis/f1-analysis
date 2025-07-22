from src.scrapers.race_scraper import scrape_race_data
from src.scrapers.racetrack_scraper import scrape_racetrack_data
from src.scrapers.weather_scraper import scrape_weather_data, get_only_needed_weather_data
from src.utils.json_util import *
from src.utils.race_util import Race
from src.scrapers.team_scraper import get_all_teams

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.widgets import Button
from matplotlib.ticker import MultipleLocator
from sklearn.preprocessing import PolynomialFeatures

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
    
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)  # X is your input variable

    model = LinearRegression()
    model.fit(X_poly, y)
    y_pred = model.predict(X_poly)
    
    # Generate a smooth range of X values for plotting the curve
    X_range = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    X_range_poly = poly.transform(X_range)
    y_range_pred = model.predict(X_range_poly)
    
    # Calculate R^2 and RMSE
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    ax.scatter(X, y, label='Actual')
    ax.plot(X_range, y_range_pred, color='red', label='Regression curve')
    ax.set_title(f'{teams[team_index]} vs {target}')
    ax.set_xlabel(target)
    ax.set_ylabel(teams[team_index])
    ax.set_ylim(0.5, 20.5)
    ax.yaxis.set_major_locator(MultipleLocator(2)) 
    ax.legend()
    
    # Show R^2 and RMSE on the plot
    textstr = f'$R^2$: {r2:.3f}\nRMSE: {rmse:.3f}'
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
      verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
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