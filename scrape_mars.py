# Import BeautifulSoup for parsing and splinter for site navigation
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests
import time 

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary of all the scaped data
    listings = {}

    # Mars news
    nasaurl = "https://mars.nasa.gov/news/"
    browser.visit(nasaurl) 
    html = browser.html
    soup = bs(html, 'html.parser')

    # Save the most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    
    # Add the news info to the dictionary
    listings["news_date"] = news_date
    listings["news_title"] = news_title
    listings["news_summary"] = news_p

    
    # Visit the JPL NASA Mars URL
    jplurl = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jplurl)
    html = browser.html
    soup = bs(html, 'html.parser')
    dataurl = 'https://www.jpl.nasa.gov'+ soup.find('a', class_='button fancybox').get("data-link")
    dataurl

    # Get full sized feature image
    browser.visit(dataurl)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_="main_image").get("src")
    featured_image = 'https://www.jpl.nasa.gov'+ image
    listings["featured_image_url"] = featured_image


    # Mars Weather using Twitter
    twitterurl = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(twitterurl)

    # Create BeautifulSoup object; parse with 'html.parser'
    twittersoup = bs(response.text, 'html.parser')
    mars_weather = twittersoup.find_all('div', class_="js-tweet-text-container")[0].p.text
    listings["mars_weather"] = mars_weather


    # Mars Facts
    marsfacturl = 'https://space-facts.com/mars/'
    marstables = pd.read_html(marsfacturl)
    marstables

    marsdf = marstables[0]
    marsdf.columns = ['Category', 'Facts']
    marsdf.set_index('Category', inplace=True)
    html_table = marsdf.to_html()
    html_table.replace('\n', '')
    listings["mars_table"] = html_table
    
 
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    usgsurl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgsurl)

    hemisphere=[]

    for i in range (4):
        time.sleep(3)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        link = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ link
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere.append(dictionary)
        browser.back()
    
    listings["hemisphere"] = hemisphere

    return listings
    