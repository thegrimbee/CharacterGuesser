import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://ideas.time.com/2013/12/10/whos-biggest-the-100-most-significant-figures-in-history/'
json_path = "C:/Users/gabri/Downloads/CharacterGuesser/characters.json"

with open(json_path, 'r') as json_file:
    characters = json.load(json_file)

# Send a GET request to the URL


# Check if the request was successful

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    names = soup.find_all('p')
    for name in names:
        name = name.get_text().strip().split()
        if name[0].isnumeric():
            name = ' '.join(name[1:])
            characters['historical figures'].append(name)
            print('Added ' + name)
else:
    print('Failed to retrieve the webpage')

with open(json_path, 'w') as json_file:
    json.dump(characters, json_file, indent=4)