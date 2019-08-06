import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from datetime import datetime


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/Users/pyash/Desktop/learnpython/12-Web-Scraping-and-Document-Databases/3/Activities/Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    allData = {}
    newsOuput = MarsNews()
    hemisphereOutput = MarsHemispheres()
    allData = {
        'news_title': newsOuput[0],
        'news_p': newsOuput[1],
        'featured_image_url': FeaturedImage(),
        'mars_weather': MarsWeather(),
        'MarsFactsTables': MarsFacts(),
        'hemisphere_image_firstURL': hemisphereOutput[0].get('img_url'),
        'hemisphere_image_secondURL': hemisphereOutput[1].get('img_url'),
        'hemisphere_image_thirdURL': hemisphereOutput[2].get('img_url'),
        'hemisphere_image_fourthURL': hemisphereOutput[3].get('img_url'),
        'hemisphere_image_firstTitle': hemisphereOutput[0].get('title'),
        'hemisphere_image_secondTitle': hemisphereOutput[1].get('title'),
        'hemisphere_image_thirdTitle': hemisphereOutput[2].get('title'),
        'hemisphere_image_fourthTitle': hemisphereOutput[3].get('title')
        
    }
    return(allData)

def MarsNews():
    browser = init_browser()
    urlNews = 'https://mars.nasa.gov/news/'
    browser.visit(urlNews)
    htmlNews = browser.html
    soupCleanNews = BeautifulSoup(htmlNews, 'html.parser')
    resultsCleanNews = soupCleanNews.find_all('div', class_="list_text")
    allDataDate = []
    allDataText = []
    allDataURL = []
    allDataURLTeaser = []

    for i in resultsCleanNews:
        try:
            dateText = datetime.strptime(i.find('div',class_="list_date").text, '%B %d, %Y')
            urlText = 'https://mars.nasa.gov' + i.a['href']
            titleText = i.find('a').text
            teaserText = i.find('div', class_='article_teaser_body').text
            allDataDate.append(dateText)
            allDataText.append(titleText)
            allDataURL.append(urlText)
            allDataURLTeaser.append(teaserText)
        except AttributeError as e:
            print(e)
            
    marsNewsDT = pd.DataFrame({
        'Date': allDataDate,
        'Title': allDataText,
        'Teaser' : allDataURLTeaser,
        'URL' : allDataURL
    })
    RelNewsData = marsNewsDT[marsNewsDT.Date==max(marsNewsDT.Date)]
    news_title = RelNewsData.iat[0,1].strip()
    news_p = RelNewsData.iat[0,2].strip()
    newsList = [news_title,news_p]
    browser.quit()
    return(newsList)

def FeaturedImage():
    browser = init_browser()
    urlFeaturedImage = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(urlFeaturedImage)
    htmlurlFeaturedImage = browser.html
    soupCleanFeaturedImage = BeautifulSoup(htmlurlFeaturedImage, 'html.parser')
    FeaturedImage = soupCleanFeaturedImage.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + FeaturedImage
    browser.quit()
    return(featured_image_url)

def MarsWeather():
    browser = init_browser()
    urlTwitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(urlTwitter)
    htmlTwitter = browser.html
    soupCleanTwitter = BeautifulSoup(htmlTwitter, 'html.parser')
    resultsTwitter = soupCleanTwitter.find_all('div', class_="js-tweet-text-container")
    tweetList = []
    for i in resultsTwitter:
        tweetText = i.find('p').text
        if 'InSight sol' in tweetText:
            tweetTextMod = tweetText.replace('\n',' ')
            tweetTextMod = tweetText.replace('hPa','hpa|')
            tweetTextMod = tweetTextMod.split('|', 1)[0].strip()
            tweetList.append(tweetTextMod)
    mars_weather = tweetList[0]
    browser.quit()
    return(mars_weather)

def MarsFacts():
    urlFacts = 'https://space-facts.com/mars/'
    FactsTables = pd.read_html(urlFacts)
    MarsFactsTables = FactsTables[1]
    MarsFactsTables.columns = ['Facts', 'Values']
    MarsFactsTables = MarsFactsTables.to_html(index = False)
    return(MarsFactsTables)

def MarsHemispheres():
    browser = init_browser()
    urlHemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(urlHemispheres)
    htmlHemispheres = browser.html
    soupCleanHemispheres = BeautifulSoup(htmlHemispheres, 'html.parser')
    browser.quit()
    resultsHemispheresURL = soupCleanHemispheres.find_all('a', class_="itemLink product-item")
    hemisphere_image_urls = []
    for i in range(len(resultsHemispheresURL)):
        if i % 2 == 1:
            hemisphereText = resultsHemispheresURL[i].text
            hemisphereURL = 'https://astrogeology.usgs.gov' + resultsHemispheresURL[i]['href']
            browser = init_browser()
            browser.visit(hemisphereURL)
            htmlHemispheresIMAGE = browser.html
            soupCleanHemispheresIMAGE = BeautifulSoup(htmlHemispheresIMAGE, 'html.parser')
            browser.quit()
            resultsHemispheresIMAGEURL = soupCleanHemispheresIMAGE.find_all('li')
            for i in resultsHemispheresIMAGEURL:
                if i.find('a').text == 'Sample':
                    hemisphereIMAGEURL = i.a['href']
                    hemisphere_image_urls.append({'title' : hemisphereText.strip(), 'img_url' : hemisphereIMAGEURL.strip()})
                    
    return(hemisphere_image_urls)


