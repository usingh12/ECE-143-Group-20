import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from preprocess import preprocess

def get_food_popularity_graph(countries):
    '''
    This function takes in 2 lists of strings as an input. One 
    is a list of all the countries we are analyzing, and the second
    one is a list of pickle files that contain nutritional facts
    about that country. Finally it will output a graph displaying
    the popularity of the foods across different countries in a 
    bar chart format.
    
    Args:
    countries: list of strings representing countries

    Returns:
    '''

    assert(isinstance(countries,list)), "countries has to of type list"
    assert(all(isinstance(x, str) for x in countries)), 'all contents of countries need to be of type string'

    files = [os.path.join('./data', 'allrecipes_' + country + '.pkl') for country in countries]
    
    #Analysis section
    rating_dict = {}
    for i in range(len(countries)):
        pickle_in = open(files[i],'rb')
        pickle_example = pickle.load(pickle_in)
        contents = preprocess(pickle_example)
        sum_rating = float(0)
        for j in range(len(contents)):
            if (not(math.isnan(contents[j]['rating']))):
                sum_rating = sum_rating + contents[j]['rating']

        rating_dict[countries[i]] = sum_rating/len(contents)

    rating_tuples = sorted(rating_dict.items(), key = lambda kv:(kv[1], kv[0])) 


    #Plotting Section
    plt.rcdefaults()
    fig, ax = plt.subplots()
    x = []
    people = []
    
    for i in rating_tuples:
        people.append(i[0])
	

    for i in people:
        x.append(rating_dict[i])
    y_pos = np.arange(len(people))

    bar = ax.barh(y_pos, x,color='blue' ,align='center')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.set_xlim(3, 5)
    ax.set_xlabel('Average Rating')
    ax.set_title('Food Ratings')
    
    y = []
    for i in people:
        g = float("{0:.3f}".format(rating_dict[i]))
        y.append(g)


    for i, v in enumerate(y):
        ax.text(v, i , str(v), color='black', fontweight='bold')

    plt.show()


#if __name__ == '__main__':
    #files_names=['data/allrecipes_China.pkl','data/allrecipes_France.pkl','data/allrecipes_Greece.pkl','data/allrecipes_India.pkl','data/allrecipes_Italy.pkl','data/allrecipes_Japan.pkl','data/allrecipes_Korea.pkl','data/allrecipes_Mexico.pkl','data/allrecipes_Thai.pkl','data/allrecipes_US.pkl']    
    #country_names = ['China','France','Greece','India','Italy','Japan','Korea','Mexico','Thai','US']
    #get_food_popularity_graph(country_names,files_names)

