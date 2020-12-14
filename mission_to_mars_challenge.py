#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


df.to_html()

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = BeautifulSoup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# #### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
short_url = 'https://astrogeology.usgs.gov'

# 2. Create a list to hold the images and titles.
browser.visit(url)
html = browser.html
img = BeautifulSoup(html, 'html.parser')
main_url = img.find_all('div', class_ ='item')
titles=[]
hemisphere_img_urls=[]

for x in main_url:
    title = x.find('h3').text
    url = x.find('a')['href']
    hem_img_url= short_url + url
    #print(hem_img_url)
    browser.visit(hem_img_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_img_original= soup.find('div',class_='downloads')
    hemisphere_img_url=hemisphere_img_original.find('a')['href']
    
    print(hemisphere_img_url)
    img_data=dict({'title':title, 'img_url':hemisphere_img_url})
    hemisphere_img_urls.append(img_data)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_img_urls

# 5. Quit the browser
browser.quit()



