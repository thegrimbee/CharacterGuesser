import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://myanimelist.net/character.php'
class_id = 'fs14 fw-b'
json_path = "C:/Users/gabri/Downloads/CharacterGuesser/characters.json"

with open(json_path, 'r') as json_file:
    characters = json.load(json_file)

# Send a GET request to the URL


# Check if the request was successful
limit = 0
while (limit < 1000):
    response = requests.get(url + '?limit=' + str(limit))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        names = soup.find_all(class_ = class_id)
        for name in names:
            name = name.get_text()
            characters['anime'].append(name)
            print('Added ' + name)
        

    else:
        print('Failed to retrieve the webpage')
    limit += 50

with open(json_path, 'w') as json_file:
    json.dump(characters, json_file, indent=4)