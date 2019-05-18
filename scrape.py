import requests
import os
import pickle
import time

from urllib.request import urlopen
from tqdm import tqdm
from bs4 import BeautifulSoup

contents = []
# urls = [ 'https://www.allrecipes.com/recipe/231509']

url_list = []
with open('./urlList.pkl', 'rb') as f:
    url_list = pickle.load(f)
print(len(url_list))

t = tqdm(url_list[49500:-1])
for url in t:

    t.set_description(url)
    page = urlopen(url)
    # with open('text.txt', 'w') as out:
    #     out.write(page.read().decode('utf-8'))
    Soup = BeautifulSoup(page, 'html.parser')

    if Soup.find('span', attrs={'itemprop': 'calories'}) == None:
        continue

    catagories_list = []
    catagories = Soup.find_all(name = 'span', attrs={'class': 'toggle-similar__title'})
    for item in catagories:
        catagories_list.append(item.text.strip())

    ingredients_list = []
    ingredients = Soup.find_all(name = 'span', attrs={'class': 'recipe-ingred_txt added'})
    for item in ingredients:
        ingredients_list.append(item.text.strip())


    review_list = []
    # review_urls = Soup.find_all(name = 'a', attrs={'class': 'review-detail__link'})
    # for item in review_urls:
    #     review_page = urlopen(item['href'])
    #     review_soup = BeautifulSoup(review_page, 'html.parser')
    #     review = review_soup.find('p', attrs={'itemprop': 'reviewBody'}).text.strip()
    #     rating = review_soup.find('meta', attrs={'itemprop': 'ratingValue'})['content']
    #     review_list.append((int(rating), review))
    #     time.sleep(1)
    reviews = Soup.find_all(name = 'a', attrs={'class': 'review-container clearfix'})
    for item in reviews:
        review_rating = item.find('meta', attrs={'itemprop': 'ratingValue'})['content']
        review = item.find('p', attrs={'itemprop': 'reviewBody'}).text.strip()
        review_list.append((int(review_rating), review))

    title = Soup.find(name = 'title').text
    rating = Soup.find('meta', attrs={'itemprop': 'ratingValue'})['content']
    calories = Soup.find('span', attrs={'itemprop': 'calories'}).text
    fat = Soup.find('span', attrs={'itemprop': 'fatContent'}).text
    carbohydrate = Soup.find('span', attrs={'itemprop': 'carbohydrateContent'}).text
    protein = Soup.find('span', attrs={'itemprop': 'proteinContent'}).text
    cholesterol = Soup.find('span', attrs={'itemprop': 'cholesterolContent'}).text
    sodium = Soup.find('span', attrs={'itemprop': 'sodiumContent'}).text

    recipe = {}
    recipe['link'] = url
    recipe['title'] = title
    recipe['reviews'] = review_list
    recipe['ingreients'] = ingredients_list
    recipe['catagories'] = catagories_list
    recipe['rating'] = float(rating)

    # recipe['calories'] = float(calories.split()[0])
    # recipe['fat'] = float(fat.split()[0])
    # recipe['carbohydrate'] = float(carbohydrate.split()[0])
    # recipe['protein'] = float(protein.split()[0])
    # recipe['cholesterol'] = float(cholesterol.split()[0])
    # recipe['sodium'] = float(sodium.split()[0])

    recipe['calories'] = calories
    recipe['fat'] = fat
    recipe['carbohydrate'] = carbohydrate
    recipe['protein'] = protein
    recipe['cholesterol'] = cholesterol
    recipe['sodium'] = sodium

    contents.append(recipe)
    with open('./allrecipes.pkl', 'wb') as f:
        pickle.dump(contents, f)
    time.sleep(2)

# print(Soup.text)
# print(Soup.find('span', attrs={'itemprop': 'calories'}).text)
# print(Soup.find('span', attrs={'itemprop': 'fatContent'}).text)
# print(type(Soup.find('span', attrs={'itemprop': 'fat'})))
# print(Soup.find('title') == None)
# print(Soup.find('title').text)

with open('./allrecipes.pkl', 'wb') as f:
    pickle.dump(contents, f)

with open('./allrecipes.pkl', 'rb') as f:
    contents_load = pickle.load(f)

print(len(contents_load))
