from playwright.sync_api import sync_playwright
from race_util import *
from json_util import *

def get_race_results(url):
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

def get_race_name(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)

def get_race_links(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("table.f1-table.f1-table-with-data")
    
    race_elements = page.locator("table.f1-table.f1-table-with-data tbody tr").all()
    
    links = []
    
    for race_elemnt in race_elements:
      link = race_elemnt.locator("td:nth-child(1) a").get_attribute('href')
      
      links.append(link)
      
  return links

def get_racetrack_links(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("div.row div.col.main-column div:nth-child(2) div.col div:nth-child(1)")
    
    racetrack_elements = page.locator("div.col.main-column div:nth-child(2) div.col div:nth-child(1) a").all()
    
    links = []
    
    for racetrack_element in racetrack_elements:
      link = racetrack_element.get_attribute('href')
      
      links.append("https://ff1gp.com" + link)
      
    return links

def get_city(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("table.table.table-striped.table-hover.table-lg tbody tr:nth-child(2) td:nth-child(2)")
    
    city = page.locator("table.table.table-striped.table-hover.table-lg tbody tr:nth-child(2) td:nth-child(2)").inner_text()
    
    return city

def get_coordinates(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("table.table.table-striped.table-hover.table-lg tbody tr:nth-last-child(1) td:nth-child(2) button")
    
    coordinate_element = page.locator("table.table.table-striped.table-hover.table-lg tbody tr:nth-last-child(1) td:nth-child(2) button")
    
    latitude = coordinate_element.get_attribute('data-lat')
    longitude = coordinate_element.get_attribute('data-lng')
    
    return [latitude, longitude]

def main():
  print("Scraping racetracks...")
  
  race_links = get_racetrack_links("https://ff1gp.com/circuits")
  
  print(race_links)
  
  racetracks = []
  
  for race_url in race_links:
    city = get_city(race_url).split(", ")[0]
    print(city)
    [latitude, longitude] = get_coordinates(race_url)
    
    racetracks.append(Racetrack(city, latitude, longitude))
  
  save_to_json(convert_object_list_to_dict_list(racetracks), "racetracks")
  
  print("Scraping complete!")
  
if __name__ == "__main__":
  main()