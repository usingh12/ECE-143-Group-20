import requests
import os
import pickle
import time

from tqdm import tqdm
from bs4 import BeautifulSoup

contents = []
urls = [ 'https://www.allrecipes.com/recipe/231509',
         'https://www.allrecipes.com/recipe/250000',
         'https://www.allrecipes.com/recipe/6728']

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'referer': "https://www.allrecipes.com/" }

base_url = 'https://www.allrecipes.com/recipe/'
for i in tqdm(range(100000, 100050)):

    url = base_url + str(i)
    start_html = requests.get(url,  headers=headers)
    Soup = BeautifulSoup(start_html.text, 'html.parser')

    if Soup.find('span', attrs={'itemprop': 'calories'}) == None:
        continue

    recipe = {}
    recipe['link'] = url
    recipe['title'] = Soup.find(name = 'title').text

    calories = Soup.find('span', attrs={'itemprop': 'calories'}).text
    fat = Soup.find('span', attrs={'itemprop': 'fatContent'}).text
    carbohydrate = Soup.find('span', attrs={'itemprop': 'carbohydrateContent'}).text
    protein = Soup.find('span', attrs={'itemprop': 'proteinContent'}).text
    cholesterol = Soup.find('span', attrs={'itemprop': 'cholesterolContent'}).text
    sodium = Soup.find('span', attrs={'itemprop': 'sodiumContent'}).text

    recipe['calories'] = float(calories.split()[0])
    recipe['fat'] = float(fat.split()[0])
    recipe['carbohydrate'] = float(carbohydrate.split()[0])
    recipe['protein'] = float(protein.split()[0])
    recipe['cholesterol'] = float(cholesterol.split()[0])
    recipe['sodium'] = float(sodium.split()[0])

    contents.append(recipe)
    time.sleep(3)

# print(Soup.text)
# print(Soup.find('span', attrs={'itemprop': 'calories'}).text)
# print(Soup.find('span', attrs={'itemprop': 'fatContent'}).text)
# print(type(Soup.find('span', attrs={'itemprop': 'fat'})))
# print(Soup.find('title') == None)
# print(Soup.find('title').text)

with open('./allrecipes_sample.pkl', 'wb') as f:
    pickle.dump(contents, f)

with open('./allrecipes_sample.pkl', 'rb') as f:
    contents_load = pickle.load(f)

print(len(contents_load))
print(contents_load)
