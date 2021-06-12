from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


url = 'https://mars.nasa.gov/news/'
browser.visit(url)

html=browser.html
soup=BeautifulSoup(html,'html.parser')

#look for news titles
titles=soup.find_all('div', class_='content_title')

#look for paragraph text
paragraph=soup.find_all('div', class_='article_teaser_body')

#assign variables
news_title=titles[0].text
news_paragraph=paragraph[0].text


#Mars Image
urls = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(urls)

browser.click_link_by_partial_text('FULL IMAGE')

overlay_soup=BeautifulSoup(browser.html, 'html.parser')
img_url=overlay_soup.find_all('img', class_='fancybox-image')[0]['src']
full_url=urls.replace('index.html', '')+img_url


#Mars Facts
browser.visit('https://space-facts.com/mars/')


html=browser.html
soup=BeautifulSoup(html,'html.parser')

table=soup.find("table",{"id":"tablepress-p-mars-no-2"})

data_frame = pd.read_html(str(table))[0]

#Mars Hemispheres

url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_url=[] #create an empty list
hemisphere_soup=BeautifulSoup(browser.html, 'html.parser') #soup the browswer's current html
descriptions_list=hemisphere_soup.find_all('div', class_='description') #find div>>description
for each_description in descriptions_list: 
    hemisphere_dict={}
    hemisphere_dict['title']=each_description.find('h3').text
    hemisphere_image_url.append(hemisphere_dict)
hemisphere_image_url

for each_image in hemisphere_image_url: 
    browser.click_link_by_partial_text(each_image['title'])
    each_image['url']=browser.find_by_text('Sample').first['href']
    browser.back()

mars_data={
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "full_url":full_url,
    "data_frame":data_frame,
    "hemispheres":hemisphere_image_url

}

browser.quit()





