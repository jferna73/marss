

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    nasa_mars_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    mars_twitter = "https://twitter.com/MarsWxReport?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"


    browser.visit(nasa_mars_url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    images = soup.find_all('img')



    print(soup.prettify())


    # # Nasa Mars News


    soup.find_all('li', class_="slide")



    news_title = soup.find_all('div', class_="content_title")[1].text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(news_title)
    print(news_p)


    # # JPL Mars Space Images - Featured Image

    browser.visit(image_url)

    time.sleep(2)

    images_html = browser.html
    images_soup = BeautifulSoup(images_html, 'html.parser')



    print(images_soup.prettify())


    images_soup.find("article", class_="carousel_item")


    featured_image_url_link = images_soup.find("article", class_="carousel_item").get("style").split("'")[1]


    featured_image_url = f'https://jpl.nasa.gov{featured_image_url_link}'


    # # Mars Weather Twitter


    browser.visit(mars_twitter)

    time.sleep(2)

    mars_twitter_html = browser.html
    mars_twitter_soup = BeautifulSoup(mars_twitter_html, 'html.parser')

    mars_weather_scrape = mars_twitter_soup.find_all("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")


    mars_weather = mars_weather_scrape[0].text



    mars_weather


    # # Mars Facts


    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts_df = pd.read_html(mars_facts_url)[0]


    mars_facts_df


    html_table = mars_facts_df.to_html()

    mars_facts_html = open("mars_facts_table.html","w")
    mars_facts_html.write(html_table)
    mars_facts_html.close()


    # # Mars Hemispheres


    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    time.sleep(2)

    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')


    hemisphere_image_tags = hemispheres_soup.find_all("img", class_="thumb")


    hemisphere_image_tags

    hemisphere_images_list = []
    for i in range(len(hemisphere_image_tags)):
        oxford_dictionary = {"title":hemisphere_image_tags[i].get("alt") ,                         "img_url":f"https://astrogeology.usgs.gov{hemisphere_image_tags[i].get('src')}"}
        hemisphere_images_list.append(oxford_dictionary)


    # # List of Scrapped Data

    # # NASA Mars News: news_title and news_p
    # news_title = soup.find_all('div', class_="content_title")[1].text
    # news_p = soup.find("div", class_="article_teaser_body").text


    # # JPL Mars Space Images (featured_image_url)
    # featured_image_url_link = images_soup.find("article", class_="carousel_item").get("style").split("'")[1]
    # featured_image_url = f'jpl.nasa.gov{featured_image_url}'


    # # Mars Weather
    # mars_weather = mars_weather_scrape[0].text


    # # Mars Facts
    # mars_facts_url = "https://space-facts.com/mars/"
    # mars_facts_df = pd.read_html(mars_facts_url)[0]


    # # Mars Hemispheres (hemisphere_image_urls)
    # hemisphere_images_list

    # Store all data in a dictionary:
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_url":mars_facts_url,
        "hemisphere_images_list": hemisphere_images_list
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data


