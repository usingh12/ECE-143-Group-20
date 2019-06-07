from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import time
from tqdm import tqdm

def scrapeURL(root_url, num_pages, save_path):
    '''
    Scrapping a url list of recipes

    Parameters
    ----------
    root_url: str
    - A root url str where it gets the urls of recipes

    num_pages: int
    - The number of pages to scrape

    save_path: str
    - A filepath that saves the scrapped url list

    Example
    -------
    scrapeURL('https://www.allrecipes.com/recipes/17138/world-cuisine/european/french/main-dishes/?page=', 10, 'url_France.pkl')
    '''

    assert isinstance(root_url, str)
    assert isinstance(num_pages, int) and num_pages > 0
    assert isinstance(save_path, str)

    urlList = []

    for i in tqdm(range(1, num_pages + 1)):
        url = root_url + str(i)

        #Query the website and return the html to the variable 'page'
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        htmlUrls = soup.find_all('div', {'class': "fixed-recipe-card__info"})

        for html in htmlUrls:
            temp = html.find('a')
            temp_text = temp.get('href')
            if temp_text != None:
                urlList.append(temp_text)

        time.sleep(1)

    with open(save_path, 'wb') as f:
        pickle.dump(urlList, f)

    # save text list
    # with open("url_France.txt" , 'a') as out:
    #     for url in urlList:
    #         out.write(url + '\n')
