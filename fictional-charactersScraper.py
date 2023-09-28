import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage you want to scrape
url = 'https://definitivedose.com/the-100-most-iconic-fictional-characters/'
json_path = "C:/Users/gabri/Downloads/CharacterGuesser/characters.json"

with open(json_path, 'r') as json_file:
    characters = json.load(json_file)

# Send a GET request to the URL


# Check if the request was successful

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('li')
    for element in elements:
        if "Created by" not in element.get_text():
            continue
        name = element.get_text().strip().split()
        correct_name = ""
        for i in range(len(name)):
            if name[i][0] == '(':
                correct_name = ' '.join(name[:i])
                break
        characters['fictional characters'].append(correct_name)
        print('Added ' + correct_name)

else:
    print('Failed to retrieve the webpage')

with open(json_path, 'w') as json_file:
    json.dump(characters, json_file, indent=4)