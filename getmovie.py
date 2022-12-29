import numpy as np
import pandas as pd
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import imdb
from tqdm import tqdm
import warnings
import chromedriver_autoinstaller


import requests
import wget
import zipfile
import os

# get the latest chrome driver version number
url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
response = requests.get(url)
version_number = response.text

# build the donwload url
download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"

# download the zip file using the url built above
latest_driver_zip = wget.download(download_url,'chromedriver.zip')

# extract the zip file
with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
    zip_ref.extractall("driver") # you can specify the destination folder path here
# delete the zip file downloaded above
#os.remove(latest_driver_zip)


os.environ["PATH"] = "/driver/chromedriver.exe"

warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")


driver = webdriver.Chrome(executable_path="driver/chromedriver.exe",options=options)


def GetMovie(name)->list:
    global driver
    ia = imdb.IMDb()

    search = ia.search_movie(name)

    try:
        movie_name = search[0]
    except:
        return "Movie Not Found"," - "," - "

    id = movie_name.movieID	
    year = movie_name.data["year"]

    url = f'https://www.imdb.com/title/tt{id}/reviews?ref_=tt_ov_rt'

    driver.get(url)

    print(driver.title)

    sel = Selector(text = driver.page_source)
    review_counts = sel.css('.lister .header span::text').extract_first().replace(',','').split(' ')[0]
    more_review_pages = int(int(review_counts)/25)



    for i in tqdm(range(more_review_pages)):
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()
        except:
            pass

    try:
        reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
        first_review = reviews[0]
        sel2 = Selector(text = first_review.get_attribute('innerHTML'))
    except Exception as e:
        print(e)
        return "No Reviews Found",str(movie_name),year



    review_list = []

    error_url_list = []
    error_msg_list = []
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

    for d in tqdm(reviews):
        try:
            sel2 = Selector(text = d.get_attribute('innerHTML'))

            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN
           
            review_list.append(review)
            
        except Exception as e:
            error_url_list.append(url)
            error_msg_list.append(e)



    print(review_list)

    return review_list,str(movie_name),year


if __name__ == "__main__":
    GetMovie("naane varuvn")
