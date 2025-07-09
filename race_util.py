from json_util import convert_object_list_to_dict_list

class Driver:
  def __init__(self, name: str, team: str, pos: int):
    self.name = name
    self.team = team
    self.pos = pos
  
  def __str__(self):
    return f"{self.name} - {self.team} - {self.pos}"
  
  def __repr__(self):
    return f"{self.name} - {self.team} - {self.pos}"
  
  def to_dict(self):
    return {
      "name": self.name,
      "team": self.team,
      "pos": self.pos
    }
    
class Race:
  def __init__(self, city: str, date_start: str, date_end:str, race_result: list[Driver]):
    self.city = city
    self.date_start = date_start
    self.date_end = date_end
    self.race_result = race_result
  
  def __str__(self):
    return f"{self.city} - {self.date_start} - {self.date_end}"
  
  def __repr__(self):
    return f"{self.city} - {self.date_start} - {self.date_end}"
  
  def to_dict(self):
    return {
      "city": self.city,
      "date_start": self.date_start,
      "date_end": self.date_end,
      "race_result": convert_object_list_to_dict_list(self.race_result)
    }
    
class Racetrack:
  def __init__(self, city, latitude, longitude):
    self.city = city
    self.latitude = latitude
    self.longitude = longitude
  
  def __str__(self):
    return f"{self.city} - {self.date_start} - {self.date_end}"
  
  def __repr__(self):
    return f"{self.name} - {self.date_start} - {self.date_end}"