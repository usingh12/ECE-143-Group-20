import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string

import wordcloud
from collections import defaultdict
from PIL import Image

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from preprocess import preprocess

class plot_wordcloud:
    
    def __init__(self, country):
        '''
        Intialization function
        
        Parameters
        ----------
        country: str
        - The country you want to plot word cloud.
        '''
        
        assert country in ['India', 'Japan', 'Korea', 'China', 'Thai', 'Italy', 'France', 'Greece', 'Mexico', 'US']
        
        with open('./data/allrecipes_' + country + '.pkl', 'rb') as f:
            self.df = pd.DataFrame(preprocess(pickle.load(f)))['ingredients']

    def count_ingredients(self, log_scale=True):
        '''
        Count the frequenciese of the ingredients
        
        Parameters
        ----------
        log_scale: bool
        - If True, apply log to frequencies.
        
        Returns
        -------
        freqs: dict
        - A dict of number of frequences of each ingredient
        '''
        
        assert isinstance(log_scale, bool)
        
        food = wordnet.synset('food.n.02')

        ingredients = self.df.sum()
        ingredients = [x.lower() for x in ingredients]
        punc_table = str.maketrans({key: None for key in string.punctuation + string.digits})
        ingredients = [word.translate(punc_table) for word in ingredients]

        food_words = list(set([w.lower() for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
        unwanted_words = ['greens','green','pepper','cut','chili','chile', 'soy', 'cayenne']
        ingredients = [word for word in ingredients if word in food_words and not word in unwanted_words]

        freqs = defaultdict(int)
        for word in ingredients:
            freqs[word] += 1
            
        # Apply log scale
        if log_scale:
            for word in freqs.keys():
                freqs[word] = np.log(freqs[word] + 1) + 1

        return freqs
    
    def plot_wordcloud(self, background='./img/India.png', save_path='./img/wc.png', log_scale=True):
        '''
        Plot wordcloud of ingredients
        
        Parameters
        ----------
        background: str
        - A filepath of the background image
        
        save_path: str
        - A filepath to save wordcloud image
        
        log_scale: bool
        - If True, apply log to frequencies.
        '''
        
        assert isinstance(background, str)
        assert isinstance(log_scale, bool)
        
        mask = np.array(Image.open(background).convert('RGB'))
        height = mask.shape[0]
        width = mask.shape[1]
        wc = wordcloud.WordCloud(background_color="black", 
                                 width=width, 
                                 height=height, 
                                 max_words=1000, 
                                 min_font_size=height / 28)
        wc.generate_from_frequencies(self.count_ingredients(log_scale = log_scale))

        plt.figure(figsize=(width / 500, height / 500))
        plt.axes([0,0,1,1], frameon = True) 
        image_colors = wordcloud.ImageColorGenerator(mask)
        plt.axis('off')
        plt.autoscale(tight=True)
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.savefig(save_path, dpi=600)

if __name__ == '__main__':
	wc = plot_wordcloud('Thai')
	wc.plot_wordcloud(background = './img/Thai.png', save_path = './img/wc_Thai.png', log_scale = True)
