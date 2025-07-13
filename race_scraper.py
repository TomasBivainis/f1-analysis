from playwright.sync_api import sync_playwright
from race_util import *
from json_util import *
from date_util import *
from lang_util import *

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

def get_race_city(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("main")
    
    city = page.locator("main div.f1rd-page.contents div:nth-child(3) div:nth-child(2) p").all()[1].inner_text().split(", ")[1]
    
    return city
    
def get_race_dates(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("main")
    
    date_text_list = page.locator("main div.f1rd-page.contents div:nth-child(3) div:nth-child(2) p").all()[0].inner_text().split(" ")
    
    year = None
    month_start = None
    month_end = None
    day_start = None
    day_end = None
    
    if len(date_text_list) == 5:
      year = date_text_list[4]
      month_start = date_text_list[3]
      month_end = month_start
      day_start = date_text_list[0]
      day_end = date_text_list[2]
    else:
      year = date_text_list[5]
      month_start = date_text_list[4]
      month_end = date_text_list[1]
      day_start = date_text_list[0]
      day_end = date_text_list[3]
      
    month_start = convert_month_to_number(month_start)
    
    month_end = convert_month_to_number(month_end)
    
    return [f"{year}-{month_start}-{day_start}", f"{year}-{month_end}-{day_end}"]
    

def get_race_links(url):
  with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    page.wait_for_selector("table.f1-table.f1-table-with-data")
    
    race_elements = page.locator("table.f1-table.f1-table-with-data tbody tr").all()
    
    links = []
    
    for race_elemnt in race_elements:
      link = race_elemnt.locator("td:nth-child(1) a").get_attribute('href').replace("../", "")
      
      links.append("https://www.formula1.com/" + link)
      
  return links

def scrape_race_data():
  print("Scraping race results...")
  
  race_links = get_race_links("https://www.formula1.com/en/results/2025/races")
  
  races = []
  
  for race_url in race_links:
    city = replace_weird_characters(get_race_city(race_url))
    print(city)
    [date_start, date_end] = get_race_dates(race_url)
    results = get_race_results(race_url)
    
    races.append(Race(city, date_start, date_end, results))
  
  save_to_json(convert_object_list_to_dict_list(races), "race_results")
  
  print("Scraping complete!")
  
if __name__ == "__main__":
  scrape_race_data()