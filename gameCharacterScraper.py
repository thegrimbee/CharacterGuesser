import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://www.giantbomb.com/profile/pixel_kaiser/lists/top-100-video-game-characters-of-all-time/368337/'
json_path = "C:/Users/gabri/Downloads/CharacterGuesserBing/characters.json"

with open(json_path, 'r') as json_file:
    characters = json.load(json_file)

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    ul_element = soup.find(class_= "editorial user-list js-simple-paginator-container")
    print(ul_element)
    elements = ul_element.find_all('h3')
    for element in elements:
        element = element.get_text()
        element = element.strip().split()
        element = ' '.join(element[1:])
        characters['game character'].append(element)

else:
    print('Failed to retrieve the webpage')

with open(json_path, 'w') as json_file:
    json.dump(characters, json_file, indent=4)