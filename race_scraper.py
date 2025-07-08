from playwright.sync_api import sync_playwright
from race_util import Driver, Race
from json_util import save_to_json, convert_object_list_to_dict_list

def scrape_race_results(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("table tbody tr")
    
    driver_elements = page.locator("table tbody tr").all()
    
    driver_positions = []
    
    for driver_element in driver_elements:
      name = driver_element.locator("td:nth-child(3)").inner_text()
      team = driver_element.locator("td:nth-child(4)").inner_text()
      pos = driver_element.locator("td:nth-child(1)").inner_text()
      
      name = name.replace("\u00a0", " ")
      
      try:
        pos = int(pos)
      except:
        pos = None
      
      driver_positions.append(Driver(name, team, pos))
  
  return driver_positions
      
def main():
  print("Scraping race results...")
  
  races = {
    "Australian Grand Prix": "https://www.formula1.com/en/results/2025/races/1254/australia/race-result",
    "Chinese Grand Prix": "https://www.formula1.com/en/results/2025/races/1255/china/race-result",
    "Japanese Grand Prix": "https://www.formula1.com/en/results/2025/races/1256/japan/race-result",
    "Bahrain Grand Prix": "https://www.formula1.com/en/results/2025/races/1257/bahrain/race-result",
    "Saudi Arabian Grand Prix": "https://www.formula1.com/en/results/2025/races/1258/saudi-arabia/race-result",
    "Miami Grand Prix": "https://www.formula1.com/en/results/2025/races/1259/miami/race-result",
    "Emilia-Romagna Grand Prix": "https://www.formula1.com/en/results/2025/races/1260/emilia-romagna/race-result",
    "Monaco Grand Prix": "https://www.formula1.com/en/results/2025/races/1261/monaco/race-result",
    "Catalunya Grand Prix": "https://www.formula1.com/en/results/2025/races/1262/spain/race-result",
    "Canada Grand Prix": "https://www.formula1.com/en/results/2025/races/1263/canada/race-result",
    "Austrian Grand Prix": "https://www.formula1.com/en/results/2025/races/1264/austria/race-result",
    "British Grand Prix": "https://www.formula1.com/en/results/2025/races/1277/great-britain/race-result"
  }
  
  race_results = []
  
  for (race_name, race_url) in races.items():
    race_results.append(Race(race_name, scrape_race_results(race_url)))
  
  save_to_json(convert_object_list_to_dict_list(race_results), "race_results")
  
  print("Scraping complete!")
  
if __name__ == "__main__":
  main()