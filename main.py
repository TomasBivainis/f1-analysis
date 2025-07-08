import requests
from dotenv import load_dotenv
import os
load_dotenv()

url = os.getenv("BASE_API_URL")

response = requests.get("https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed%3E=315")

if response.status_code == 200:
  data = response.json()
  print(data)
else:
  print(f"Error: {response.status_code}")