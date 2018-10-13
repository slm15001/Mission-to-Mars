import pandas as pd
from bs4 import BeautifulSoup as bs
import time 
from splinter import Browser
from flask import Flask, jsonify, request

# def init browser
def init_browser():
    executable_path = {'executable_path': 'C:/Users/Sal/Desktop/Chrome Driver/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

# NASA Mars News
def scrape():
    # Open a blank window of Google Chrome.
    browser = init_browser()
    mars_facts_data = {}

    # Visit the NASA newspage using the blank Chrome window. 
    nasa_news_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_news_url)

    # Get html code from the site and convert it into json. 
    html = browser.html
    soup = bs(html,"html.parser")

    news_title  = soup.find("div",class_="content_title").text
    paragraph_text = soup.find("div", class_="article_teaser_body").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = paragraph_text 
    # JPL Mars Space Images - Featured Image

    # Visit the JPL site which includes the featured image and extract the html code.  
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)

    html = browser.html
    soup = bs(html,"html.parser")

    featured_image_url = soup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href') 

    split_url = featured_image_url.split('/')

    pia_url = split_url[-1]

    base_image_url = "https://photojournal.jpl.nasa.gov/jpeg/"

    pia_final = pia_url.split('_')[0]+'.jpg'

    full_image_url = base_image_url + pia_final
    mars_facts_data["featured_image_url"] = full_image_url

    # Mars Weather
    mars_weather_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_twitter_url)

    html = browser.html
    soup = bs(html,"html.parser")

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_facts_data["mars_weather"] = mars_weather
    # Mars Facts
    mars_facts_url = "https://space-facts.com/mars/"

    mars_facts_tb1 = pd.read_html(mars_facts_url)[0]
    mars_facts_tb1.columns=['Physical Properties', 'Values']
    mars_html_table = mars_facts_tb1.to_html(justify='left', index=False).replace('\n','')
    mars_facts_data["mars_facts_table"] = mars_html_table

    # Mars Hemispheres
    mars_hemi_urls = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_urls)

    html = browser.html
    soup = bs(html,"html.parser")

    #Loop through the class="item" by clicking the h3 tag and getting the title and url. 
    images = soup.find('div', class_='collapsible results')
    mars_hemi_urls = []

    for i in range(len(images.find_all("div", class_="item"))):
        time.sleep(10)
        image = browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        div = soup.find("div", class_="downloads")
        for li in div:
                link = div.find('a')
        url = link.attrs['href']
        hemispheres = {
                'title' : title,
                'img_url' : url
            }
        mars_hemi_urls.append(hemispheres)
        browser.back()
    mars_facts_data["mars_hemispheres"] = mars_hemi_urls
    browser.quit()
    return mars_facts_data

