import pickle
import os 
import pandas as pd
from math import pi
import math
import operator
import collections
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from preprocess import preprocess
    
def freq_ingredient(contents):
    '''
    This function lemmatizes the ingredient found in
    the recipe for a country and removes common,
    unwanted words from the list.
    It also extracts the 5 most commonly used
    ingredient in the recipe and sorts them.
    -------------------------------------------------
    Parameters
    contents: 
    - Type: list of dicts
    - A list of dict scraped from allrecipes.com
    -------------------------------------------------
    Returns
    ingredient_sort: 
    - Type: list of tuples
    - A list of tuples containing top 5 most frequent
      items from the scraped data.
    '''

    assert isinstance(contents, list)
    assert all([isinstance(x, dict) for x in contents])
    
    ingredients = []
    for i in range(len(contents)):
        for ingredient in contents[i]['ingredients']:
            ingredient = ingredient.split()
            ingredients += (ingredient)
            
    food = wn.synset('food.n.02')
    f = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
    
    ingredient_list = []
    for food in ingredients:
        if food in f:
            ingredient_list.append(food)
    ingredient_out = []
    
    unwanted_words=['greens','green','pepper','cut','chili','chile', 'soy','pasta','mozzerella','parmesan','mozzarella','Parmesan','beef','spaghetti','butter','cayenne','yogurt','ham','jalapeno']
    for word in ingredient_list:
        if word not in unwanted_words:
            ingredient_out.append(word)
            
    counter=collections.Counter(ingredient_out)
    sorted_x = sorted(counter.items(), key=operator.itemgetter(1))
    ingredient_sort = sorted_x[-5:]
    return ingredient_sort
            
    #return ingredient_out

def average_consumption(ingredient_sort, country_name):
    '''
    This function calcuates the avregae consumption
    of the food items for a country within a 
    particular year.
    -------------------------------------------
    Parameters
    ingredient_sort:
    - Type: List
    - A list of ingredient names scraped from 
      allrecipes.com
    country_name: 
    - Name of the country we want the food stat for.
    - Type: string
    -------------------------------------------
    Returns
    avg_consumption:
    -Type: Dictionary
    - A dictionory of ingredients as key and its average 
      consumption as the value.
    '''

    assert isinstance(ingredient_sort, list)
    assert isinstance(country_name, str)
    assert all([isinstance(x, tuple) for x in ingredient_sort])
    
    data = pd.read_csv("./data/FAO.csv", encoding='latin-1')
    llist=['Area', 'Item', 'Y2013']
    dfb = data[data['Area'] == country_name].index.values.astype(int)
    country = data.loc[dfb[0]:dfb[-1], data.columns.isin(llist)]
    Items = ['Coconuts - Incl Copra', 'Vegetables, Other','Fish, Seafood','Tomatoes and products','Butter, Ghee','Meat','Lemons, Limes and products','Wheat and products', 'Rape and Mustardseed', 'Onions']
    country = country[country.Item.isin(Items)]
    grp=country.groupby(['Item'])
    
    veg_sum = grp.get_group('Vegetables, Other').sum(axis=1).sum()
    coco_sum = grp.get_group('Coconuts - Incl Copra').sum(axis=1).sum()
    fish_sum = grp.get_group('Fish, Seafood').sum(axis=1).sum()
    meat_sum = grp.get_group('Meat').sum(axis=1).sum()
    lime_sum = grp.get_group('Lemons, Limes and products').sum(axis=1).sum()
    onion_sum = grp.get_group('Onions').sum(axis=1).sum()
    bread_sum = grp.get_group('Wheat and products').sum(axis=1).sum()
    tomato_sum = grp.get_group('Tomatoes and products').sum(axis=1).sum()
    cheese_sum = grp.get_group('Butter, Ghee').sum(axis=1).sum()
    mustard_sum = grp.get_group('Rape and Mustardseed').sum(axis=1).sum()
    
    
    ingredient_name = []
    for i in range(0,len(ingredient_sort)):
        ingredient_name.append(ingredient_sort[i][0])
    
    avg_consumption = {}
    for dish in ingredient_name:
        if dish == "lime" or dish == "lemon":
            avg_consumption['Lime'] = lime_sum
        if dish =="mustard":
            avg_consumption['Mustard'] = mustard_sum
        if dish == "vegetable":
            avg_consumption['Veggies'] = veg_sum
        if dish == "coconut":
            avg_consumption['Coconut'] = coco_sum
        if dish == 'fish':
            avg_consumption['Fish'] = fish_sum
        if dish == 'onion':
            avg_consumption['Onion'] = onion_sum
        if dish == "bread":
            avg_consumption['Bread'] = bread_sum
        if dish == "tomato":
            avg_consumption['Tomato'] = tomato_sum
        if dish == 'chicken':
            avg_consumption['Chicken'] = meat_sum
        if dish == 'cheese':
            avg_consumption['Cheese'] = cheese_sum
            
    return avg_consumption

def polar_plot(country):
    '''
    This function is used to plot the polar plot for 
    correlation of ingredient frequency and average 
    consumption of the food item.
    ----------
    Parameters:
    country:
    - Type: String
    - Name of the country we would be plotting the
      polar plot.
    '''

    assert isinstance(country, str)
    with open(os.path.join('./data', 'allrecipes_' + country + '.pkl'), 'rb') as f:
        contents = preprocess(pickle.load(f))

    country = 'Thailand' if country == 'Thai' else country
    ingredient_freq = freq_ingredient(contents)
    ingredient_consumption = average_consumption(ingredient_freq, country)
    
    categories = list(ingredient_consumption.keys())
    N = len(categories)
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
        
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories, color ='black',size=17, position=(0.5,-0.169))
    ax.set_rlabel_position(0)

    plt.yticks([1,2,3,4,5,6,7,8, 9,10,11], ["1","2","3","4","5","6","7","8", "9","10","11"], color="black", size=1)
    plt.ylim(0,11.4)
    
    #First Plot
    ingred_consumption = {}
    for key in ingredient_consumption.keys():
        ingred_consumption[key] = math.log(ingredient_consumption[key])
    values = list(ingred_consumption.values())
    values += values[:1]
    ax.plot(angles, values, linewidth=3, linestyle='solid', label="Average Consumption")
    ax.fill(angles, values, 'b', alpha=0.1)
    
    #Second Plot
    ingredient_count = []
    for i in range(0,len(ingredient_freq)):
        ingredient_count.append(ingredient_freq[i][1])
    for i in range(len(ingredient_count)):
        ingredient_count[i] = math.log(ingredient_count[i])
    values = list(ingredient_count)
    values += values[:1]
    
    ax.plot(angles, values, 'r', linewidth=3, linestyle='solid', label="Ingredient Frequency")
    ax.fill(angles, values, 'r', alpha=0.1)
    
    plt.rcParams.update({'font.size': 14})
    plt.legend(loc='upper right', bbox_to_anchor=(0, 0))


