from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

# Splinter setup as global variables
executable_path = {"executable_path" : ChromeDriverManager().install()}


# Defining a scrape function
def scrape():
    browser = Browser("chrome", **executable_path, headless = False)
    # Initalise a dictionary to store all our data from scraping
    mars_data_dict = {}

    # Call the scrape functions 
    mars_news_data = mars_news(browser)
    
    mars_data_dict["Mars_News"] = mars_news_data[0]
    print("mars_news success")
    mars_data_dict["Mars_Paragraph"] = mars_news_data[1]
    print("mars_paragraph success")
    mars_data_dict["Mars_Images"] = mars_images(browser)
    print("mars_images success")
    mars_data_dict["Mars_Facts"] = mars_facts(browser)
    print("mars_facts success")
    mars_data_dict["Mars_Hemispheres"] = mars_hemispheres(browser)
    print("mars_hemispheres success")
    # quit function
    browser.quit()
    return mars_data_dict


def mars_news(browser):
    mars_url = "https://redplanetscience.com/"
    browser.visit(mars_url)
    time.sleep(1)
    mars_html = browser.html
    mars_soup = bs(mars_html, "html.parser")
    section_browse = mars_soup.find("div", class_ = "list_text")
    title_browse = section_browse.find("div", class_ = "content_title").text
    paragraph_browse = section_browse.find("div", class_ = "article_teaser_body").text
    mars_ls = [title_browse, paragraph_browse]
    return mars_ls

def mars_images(browser):
    images_url = "https://spaceimages-mars.com/"
    browser.visit(images_url)
    time.sleep(1)
    images_html = browser.html
    images_soup = bs(images_html, "html.parser")
    div_browse = images_soup.find("div", class_ = "header")
    img_browse = div_browse.find("img", class_ = "headerimage")['src']
    featured_image_url = images_url + img_browse
    return featured_image_url

def mars_facts(browser):
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    time.sleep(1)
    tables = pd.read_html(facts_url) 
    Mars_info_df = pd.DataFrame(tables[0]) 
    Mars_info_df = Mars_info_df.rename(columns = {0 : "Description"})
    Mars_info_df = Mars_info_df.set_index("Description")
    Mars_info_table = Mars_info_df.to_html()
    return Mars_info_table

def mars_hemispheres(browser):
    mars_hemisphere_ls = []
    astro_url = "https://marshemispheres.com/"
    for i in range(4):
        browser.visit(astro_url)
        time.sleep(1)
        mars_link = browser.links.find_by_partial_text("Hemisphere")
        mars_link[i].click()
        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, "html.parser")
        title = hemisphere_soup.find("h2", class_ = "title").text
        hemisphere_img_url = hemisphere_soup.find("img", class_ = "wide-image")["src"]
        full_hemisphere_img_url = f"{astro_url}{hemisphere_img_url}"
        mars_hemisphere_ls.append({"title": title, "url": full_hemisphere_img_url})

    return mars_hemisphere_ls

