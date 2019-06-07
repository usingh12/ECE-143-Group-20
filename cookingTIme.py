import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
from preprocess import preprocess
import matplotlib.patches as mpatches

abr = {'Japan':'JPN', 'Thai':'THA', 'Italy':'ITA', 'China':'CHN', 'France':'FRC', 'Mexico':'MEX', 'Greece':'GRC','India':'IND','Korea':'KOR','USA':'USA'}

def get_cooking_time_graph(countries,files):
    '''
        This function takes in two parameters as inputs. The first one is list of strings
        representing the names of countries that we are nalyzing. The second inputs is a list of
        strings representing the list of pickle files that contain the data regarding the previous
        countries nutritional facts. The output is going to be a bar chart representing the avergae
        cooking time of each country. It will also return a dictionary made up of country names mapped
        to their respective average cooking times.

        Args:
            countries: list of strings representing countries
            files: list of strings representing pickle files

        Returns:
            Bar plot representing countries average cooking time 
            Also returns a dictionary with names of countries and their average 
            cooking time rating
    '''

    assert(len(countries)==len(files)), "length of countries and number of files don't match"
    assert(isinstance(countries,list)), "countries has to of type list"
    assert(isinstance(files,list)),"files has to be of type list"
    assert(all(isinstance(x, str) for x in countries)), 'all contents of countries need to be of type string'
    assert(all(isinstance(x, str) for x in files)), 'all contents of files need to be of type string'


    prep_time_dict = {}
    for i in range(len(countries)):
        pickle_in = open(files_names[i],'rb')
        pickle_example = pickle.load(pickle_in)
        contents = preprocess(pickle_example)
        sum_time = float(0)
        for j in range(len(contents)):

            if (not(math.isnan(contents[j]['readyin_time']))):
                sum_time = sum_time + contents[j]['readyin_time']

        prep_time_dict[country_names[i]] = sum_time/len(contents)

    working_hrs = {'Japan':1742, 'Thai':1200, 'Italy':1730, 'China':2392, 'France':1472, 'Mexico':2250, 'Greece':2035,'India':1974,'Korea':2070,'USA':2428}
    cooking_time_tuples = sorted(prep_time_dict.items(), key = lambda kv:(kv[1], kv[0])) 
    working_time_tuples = sorted(working_hrs.items(), key = lambda kv:(kv[1], kv[0]))

    high_working = {}
    low_working = {}

    for i in working_time_tuples:
        if i[1] < 1800:
            low_working[i[0]] = prep_time_dict[i[0]]
        else:
            high_working[i[0]] = prep_time_dict[i[0]]

    high_working = sorted(high_working.items(), key = lambda kv:(kv[1], kv[0])) 
    low_working = sorted(low_working.items(), key = lambda kv:(kv[1], kv[0])) 

    first_half_names = []
    first_half_times = []
    second_half_names = []
    second_half_times = []

    for i in low_working:
        first_half_names.append(abr[i[0]])
        first_half_times.append(prep_time_dict[i[0]])

    for i in high_working:
        second_half_names.append(abr[i[0]])
        second_half_times.append(prep_time_dict[i[0]])	


    fig, ax = plt.subplots()
    ax.bar(first_half_names, first_half_times,color="red")
    ax.bar(second_half_names, second_half_times,color="blue")

    ax.set(ylabel='Avg Cooking Time of Main Dishes (min)', #xlabel='Average annual hours worked Rankings',
       title='Avg Cooking Time vs Avg Working Time')
    #ax.grid()


    blue_patch = mpatches.Patch(color='blue', label='Countries Ranking 1-10 on Avg Hrs Worked Annually')
    red_patch = mpatches.Patch(color='red', label='Countries Ranking 20-40 on Avg Hrs worked Annually')
    ax.set_ylim(0, 230)
    plt.legend(handles=[blue_patch,red_patch],loc=2)

    plt.show()
    
    return prep_time_dict






    
#if __name__ == '__main__':
    #files_names=['data/allrecipes_China.pkl','data/allrecipes_France.pkl','data/allrecipes_Greece.pkl','data/allrecipes_India.pkl','data/allrecipes_Italy.pkl','data/allrecipes_Japan.pkl','data/allrecipes_Korea.pkl','data/allrecipes_Mexico.pkl','data/allrecipes_Thai.pkl','data/allrecipes_US.pkl']    
    #country_names = ['China','France','Greece','India','Italy','Japan','Korea','Mexico','Thai','USA']
    #get_cooking_time_graph(country_names,files_names)


