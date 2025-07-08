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
  def __init__(self, name: str, race_result: list[Driver]):
    self.name = name
    self.race_result = race_result
  
  def __str__(self):
    return f"{self.name}"
  
  def __repr__(self):
    return f"{self.name}"
  
  def to_dict(self):
    return {
      "name": self.name,
      "race_result": convert_object_list_to_dict_list(self.race_result)
    }