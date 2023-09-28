from bs4 import BeautifulSoup
import requests
import random

url = "https://www.bing.com/images/"
path = "C:/Users/gabri/Downloads/CharacterGuesserBing/img/"
IMG_NAME = 'ori.jpg'
NUM_OF_IMAGES = 10
response = requests.get(url)
url_results = []
# Check if the request was successful

def save_img(url):
    response = requests.get(url)
    f = open(path + IMG_NAME, 'wb')
    f.write(response.content)
    f.close()
    print("Image saved")

def img_search(query):
    url_results = []
    query = query.replace(' ', '+')
    elements = []
    while not elements:
        response = requests.get(url + "search?q=" + query + "&first=1", headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url + "search?q=" + query + "&first=1")
        elements = soup.find_all(class_ = 'img_cont hoff')
        for element in elements:
            if len(url_results) >= NUM_OF_IMAGES:
                break
            img = element.find('img')
            if 'src' in img.attrs:
                url_results.append(img['src'])
            elif 'data-src' in img.attrs:
                url_results.append(img['data-src'])
    print("Image searched")
    return url_results

def create_img(urls, num = -1):
    if num == -1:
        num = random.randint(0,NUM_OF_IMAGES-1)
    save_img(urls[num])
    print("Image created")
    return num
