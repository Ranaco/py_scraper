import re
from bs4 import BeautifulSoup
import json
import requests

s = requests.get('https://mafteiach.app/all/by_year/5711')

soup = s.content

list_of_years = []

list_of = BeautifulSoup(soup, 'html.parser')

years_list = years_list = list_of.find('div', {'id': "years"})

list_of_years = years_list.find_all("button", {"class": re.compile(r'year')})
year_dummy = list_of_years
list_of_years = []

for y in year_dummy:
    text = y.text.strip()
    list_of_years.append(text)

with open('./years/year_name.json', 'w') as jsonFile:
    file = json.dumps(list_of_years, ensure_ascii = False)
    jsonFile.write(file)


print(list_of_years)



