
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo
import requests
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def scrape():
    browser = init_browser()
    time.sleep(1)

    # Nasa Mars news
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text

    # JPL Mars Space Images - Featured Image
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    location = jpl_soup.find("img", class_="headerimage")
    part_url = location["src"]
    image_url = jpl_url + part_url

    # Mars facts
    mars_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_url)

    mars_html = browser.html
    mars_table = pd.read_html(mars_url)[0]

    # Mars Hemispheres
    galaxy_url = "https://marshemispheres.com/"
    browser.visit(galaxy_url)

    galaxy_html = browser.html
    galaxy_soup = bs(galaxy_html, 'html.parser')

    all_hemi = galaxy_soup.find("div", class_='collapsible results')
    hemisphere1 = all_hemi.find_all('a')

    hemisphere_image_urls = []
    hemi_dict = []
    mars_table = []
    for hemi in hemisphere1:
        if hemi.h3:
            title = hemi.h3.text
            hemi.click
            link = hemi["href"]
            main_url = "https://marshemispheres.com/"
            forward_url = main_url+link
            browser.visit(forward_url)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemi2 = soup.find("div", class_="downloads")
            image = hemi2.ul.a["href"]
            hemi_dict = {}
            hemi_dict["title"] = title
            hemi_dict["img_url"] = main_url + image
            hemisphere_image_urls.append(hemi_dict)
            browser.back()
        # print(hemi_dict)
        mars_data = {
            'news_title': news_title,
            'summary': news_p,
            'featured_image': image_url,
            'mars_table': mars_table,
            'hemisphere_image_urls': hemisphere_image_urls,
            'news_url': url,
            'jpl_url': jpl_url,
            'fact_url': mars_url,
            'hemisphere_url': galaxy_url}
    browser.quit()

    return mars_data
