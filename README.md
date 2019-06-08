
# Food Habit Analysis (Group 20)
## Team Memebrs
- Ali Zolfaghari 
-  Hao Peng 
-  Mingchao Liang
-  Utkarsh Singh 

## Objective 
The objective of this project was to see if there is any correlation between different countries nutritional facts and important statistical data such as, obesity rates, ingridients abundancy, popularity of different food items, and how often people work in different parts of the world.

## Dataset
-  Food Recipe was scraped from the 'allrecipes.com' website to get data for 10 countries and 15 features.
-  We are also using Obesity Rate CSV dataset and Food and Agriculture Organization of the United Nations's cosmption of food item FAO CSV dataset.
- Storing the scraped data into the pickle format.

## Methodology
- We are using Pandas to process the pickle and CSV file.
- To shorten the features of ingredient and group them into single word (i.e. Mozzarella and Parmesan grouped together into Cheese category), lemmatization was used (NLTK python library)
- Words with minimal frequency and common words ("cut", "green", "chili" etc) were discarded from the ingrdient list, to make the final processed dataset.

## Conclusion 
- The frequency of ingredients used in the recipes was proportional to abundance of the food item in that country. 
-  Asian countries had relatively lower rate of obesity. 
-  Calories, fat and protein has a high correlation with the obesity rate.
-  Average prep time of a dish was surprisingly correlated to the annual working hours.

## File Structure 
```bash
├── README.md
├── data
│   └──
├── img
│   └──
├── main.ipynb
├── plot_choropleth.py
├── plot_cooktime.py
├── plot_nutrition.py
├── plot_polar.py
├── plot_popularity.py
├── plot_wordcloud.py
├── preprocess.py
├── scrape.py
└── scrapeURL.py
```


- data --> Directory having the crwaled data in pickle format
- img --> Directory having images of the plot
- main.jpynb --> to run scripts and display plots
- preprocess.py --> outputs the data in the form of list of dictionaries
- plot_choropleth.py --> Script for geo plots of obesity rate 
- plot_cooktime.py --> Script for plots of cooktime 
- plot_nutrition.py --> Script for plots related to nutritions 
- plot_polar.py --> Scripts for polar plots of ingredients 
- plot_popularity.py --> Script for plots of popularity 
- plot_wordcloud.py --> Script for plots of ingredients wordcloud
- scrape.py --> To get the nutritional facts off of the website
- scrapeURL.py --> To get the URL for all the food items necessary 

## Instructions on running the code
> Python Version: 3.7.0

#### Python Libraries Requirements
- beautifulsoup4 >= 4.6.3
- tqdm >= 4.31.1
- urllib3 >= 1.23
- requests >= 2.19.1
- numpy >= 1.16.2
- pandas >= 0.24.2
- geopandas == 0.4.1
- nltk >= 3.3
- bokeh >= 0.13.0
- matplotlib >= 3.0.3
- wordcloud >= 1.5.0

For installing these packages, you can use either `pip3` or conda install to install packages. For example,

``` Bash
pip3 install beautifulsoup4
```

### Running the code
#### Plot 
1. Run the main.ipynb jupyter notebook to retreive all the relevant plots in the presentation slide.
2. Additional instructions about running the code have been provided in the jupyter notebook.
#### Scraping the data
1. Run scrapeURL.py script to scrape the URL list for countries from 'allrecipes' website.
> Example:
> scrapeURL('https://www.allrecipes.com/recipes/17138/world-cuisine/european/french/main-dishes/?page=', 9, 'url_France.pkl')
2. Run scrape.py to scrpate the raw data from the 'allrecipes' wbsite. It takes in the URL present in the pickle file generated from running scrapeURL.py script.
Example:
> Example:
>scrape('./data/url_France.pkl', save_path = './data/allrecipes_France.pkl')
3. Run preprocess.py to process the raw data.
> Example:
> preprocess(pickle.load(pickle_file_name))

