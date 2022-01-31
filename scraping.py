# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Set up Splinter, initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemispheres_image_urls = mars_hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {"news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemispheres": hemispheres_image_urls,
            "last_modified": dt.datetime.now()
            }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# ###Article Scraping
def mars_news(browser):
    # Visit Mars NASA news site
    url = 'http://redplanetscience.com'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Image Scraping (Featured Images)
def featured_image(browser):
    # Visit URL
    url = 'http://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ### Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Scraping data table from 'galaxyfacts' to dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Converting dataframe back to html format
    return df.to_html(classes="table table-striped")

# ### Mars Hemispheres
def mars_hemispheres(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemispheres_image_urls = []

    # Write code to retrieve the image urls and titles for each hemispheres.
    # Loop through to get 4 different images
    for i in range(4):
    
        # Create empty dictionary
        # find tags to click for different hemispheres
        # Find sample images URL and title for each hemispheres
        # Add img_url and title to dictionary and then to list
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        img_url = browser.find_link_by_text('Sample').first['href']
        title = browser.find_by_css('h2.title').text
        hemispheres["img_url"] = (img_url)
        hemispheres["title"] = title    
        hemispheres_image_urls.append(hemispheres)
        browser.back()

    return hemispheres_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


