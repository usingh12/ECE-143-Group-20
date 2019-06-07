import requests
import os
import pickle
import time

from urllib.request import urlopen
from tqdm import tqdm
from bs4 import BeautifulSoup

def scrape(url_file, save_path):
    '''
    Scraping recipes according to the given urls

    Parameters
    ----------
    url_file: str
    - A filepath of a pickle file that stores urls of recipes

    save_path: str
    - A filepath that saves the scrapped data
    '''

    assert isinstance(url_file, str)
    assert isinstance(save_path, str)

    contents = []

    with open(url_file, 'rb') as f:
        url_list = pickle.load(f)
    print(len(url_list))

    t = tqdm(url_list)
    for url in t:

        t.set_description(url)
        page = urlopen(url)
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
        reviews = Soup.find_all(name = 'div', attrs={'class': 'review-container clearfix'})
        for item in reviews:
            review_rating = item.find('meta', attrs={'itemprop': 'ratingValue'})['content']
            review = item.find('p', attrs={'itemprop': 'reviewBody'}).text.strip()
            review_list.append((int(review_rating), review))

        direction_list = []
        directions = Soup.find_all(name = 'li', attrs={'class': 'step'})
        for item in directions:
            direction = item.find('span', attrs={'class': 'recipe-directions__list--item'}).text.strip()
            direction_list.append(direction)

        preptime_item = Soup.find('time', attrs={'itemprop': 'prepTime'})
        preptime = preptime_item.find('span', attrs={'class': 'prepTime__item--time'}).text.strip() if not preptime_item == None else None
        cooktime_item = Soup.find('time', attrs={'itemprop': 'cookTime'})
        cooktime = cooktime_item.find('span', attrs={'class': 'prepTime__item--time'}).text.strip() if not cooktime_item == None else None
        readyin_time_item = Soup.find('span', attrs={'class': 'ready-in-time'})
        readyin_time = readyin_time_item.text.strip() if not readyin_time_item == None else None

        title = Soup.find(name = 'title').text
        rating = Soup.find('meta', attrs={'itemprop': 'ratingValue'})['content']
        num_servings = Soup.find('meta', attrs={'id': 'metaRecipeServings'}).get('content')

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
        recipe['directions'] = direction_list
        recipe['ingredients'] = ingredients_list
        recipe['num_servings'] = num_servings
        recipe['catagories'] = catagories_list
        recipe['rating'] = float(rating)
        recipe['preptime'] = preptime
        recipe['cooktime'] = cooktime
        recipe['readyin_time'] = readyin_time

        recipe['calories'] = calories
        recipe['fat'] = fat
        recipe['carbohydrate'] = carbohydrate
        recipe['protein'] = protein
        recipe['cholesterol'] = cholesterol
        recipe['sodium'] = sodium

        contents.append(recipe)
        with open(save_path, 'wb') as f:
            pickle.dump(contents, f)
        time.sleep(1)
