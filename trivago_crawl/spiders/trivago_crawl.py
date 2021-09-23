import scrapy
import time
import sys
from scrapy import Request
import requests
##
from urllib.parse import unquote
from ..items import TrivagoCrawlItem
##
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
##
from shutil import which
##


binary = FirefoxBinary(which('firefox')) #path/to/installed firefox binary
options = webdriver.FirefoxOptions()
# options.add_argument("--headless") #Comment this to disable headless browser.And you'll see what happened in the web-page

class  Trivago(scrapy.Spider):
    name = 'trivago'
    start_urls = [
        'https://www.trivago.com/en'
    ]
    filters = {
        "city": "Rome",
        "check_in": "2021-07-12",
        "check_out": "2021-07-16",
        "adults": 2,
        "children": 0,
        "max_price": 0,
        "currency": "USD" #option must be capital
    }

    def __init__(self):
        self.driver = webdriver.Firefox(firefox_binary=binary ,firefox_options=options)


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5) #delay
        #update the currency
        self.driver.find_element_by_id("currency").click()
        time.sleep(.5) #double click
        self.driver.find_element_by_id("currency").click()
        time.sleep(2) #delay
        cur = self.driver.find_elements_by_class_name("option")
        for i in cur:
            if i.get_attribute("value") == Trivago.filters["currency"]:
                print("Found !!")
                i.click()
                break
        time.sleep(5) #delay
        ##scroll down smoothly
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 50):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))
        ##end scroll down
        #update the destination
        self.driver.find_element_by_id("querytext").send_keys(Trivago.filters["city"])
        time.sleep(.5)
        # To avoid auto-suggesting
        sug = self.driver.find_elements_by_class_name("ssg-title")
        for i in sug:
            if i.text == Trivago.filters['city']:
                print("First occuerance !!")
                i.click()
                break
        #
        time.sleep(2) #delay
        #click search button
        self.driver.find_element_by_class_name("search-button__label").click()
        time.sleep(2) #delay
        # update url with rest of filters
        url = unquote( self.driver.current_url ) #decode the UTF-8 encoded URL
        url = url.replace(url[25:149],"") #remove search parameters part from old url
        #check if there is no childern
        if Trivago.filters['children'] > 0:
            search_para = '&aDateRange[arr]={d1}&aDateRange[dep]={d2}&aPriceRange[from]=0&aPriceRange[to]={d3}&iRoomType=7&aRooms[0][adults]={d4}&aRooms[0][children][0]={d5}'.format(
                d1 = Trivago.filters['check_in'],
                d2 = Trivago.filters['check_out'],
                d3 = Trivago.filters['max_price'],
                d4 = Trivago.filters['adults'],
                d5 = Trivago.filters['children']
            )
        else:
            search_para = '&aDateRange[arr]={d1}&aDateRange[dep]={d2}&aPriceRange[from]=0&aPriceRange[to]={d3}&iRoomType=7&aRooms[0][adults]={d4}'.format(
                d1 = Trivago.filters['check_in'],
                d2 = Trivago.filters['check_out'],
                d3 = Trivago.filters['max_price'],
                d4 = Trivago.filters['adults']
            )
        #absolute url
        abs_url = url + search_para
        abs_url = abs_url.replace("apt2", "cpt2").replace("hasMap=1", "hasMap=0") #change selenium app identity for urls
        # print("\n",abs_url,"\n")
        ##
        self.driver.get(abs_url)
        time.sleep(2) #delay
        ##
        # Trivago.get_data(self,response, abs_url)
        # print("Absolute url: \n",L_url,"\n")
        # next_page = self.driver.find_element_by_class_name('btn.btn--pagination.btn--small.btn--page-arrow.btn--next')
        item = TrivagoCrawlItem()
        # self.driver.get(url)
        while True:
            # items variables
            hotel_name = ''
            hotel_link = ''
            image_link = ''
            rating = ''
            num_of_ratings = ''
            num_of_stars = ''
            hotel_address = ''
            to_center = ''
            major_total_price = ''
            major_price_per_night = ''
            major_seller = ''
            minor_price_per_night = ''
            minor_seller = ''
            lowest_price_per_night = ''
            lowest_seller = ''
            print("\n\n\n 2 \n\n\n")
            ##            
            for i in self.driver.find_elements_by_css_selector('[data-qa="item-location-details"]'):
                try:
                    i.click()
                    time.sleep(.01)
                except:
                    pass
            print("\n\n\n 3 \n\n\n")
            ##scroll down smoothly
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            for i in range(1, total_height, 100):
                self.driver.execute_script("window.scrollTo(0, {});".format(i))
            ##end scroll down
            print("\n\n\n 4 \n\n\n")
            #yield items
            for container in self.driver.find_elements_by_css_selector('[data-qa="itemlist-element"]') :
                print("\n\n\n 5 \n\n\n")
                #get hotel name
                try:
                    hotel_name = container.find_element_by_class_name("item-link.name__copytext").text.replace(";","")
                except:
                    hotel_name = None
                ##
                #get Hotel links by id
                try:
                    hotel_id = container.get_attribute("data-item")
                    hotel_link = "https://www.trivago.com/?" + search_para + "&cpt2={d1}/100&hasList=1&hasMap=0&sharedcid={d1}&tab=info".format(d1=hotel_id)
                except:
                    hotel_link = None
                ##
                try:
                    image_link  = container.find_element_by_class_name("lazy-image__image.item__image.item__image--has-gallery").get_attribute("src") #x[0].get_attribute("src")
                except:
                    image_link  = None
                ##
                try:
                    # rating      = container.find_element_by_css_selector('[class="item-components__pillValue--8ac9c item-components__value-sm--80372 item-components__pillValue--8ac9c"]').text #x[0].text
                    rating      = container.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
                except:
                    rating      = None
                ##
                try:
                    data = container.find_element_by_class_name('details-paragraph.details-paragraph--rating').text #y[0].text.split()[1].strip("(")
                    num_of_ratings = ''.join(c for c in data if c.isdigit())
                    # x = [count for count, i in enumerate(data) if "(" in i]
                    # num_of_ratings = data[x[0]].replace("(","")
                except:
                    num_of_ratings  = None
                ##
                try:
                    num_of_stars    = container.find_element_by_css_selector(".stars-wrp meta").get_attribute("content") #y[0].get_attribute("content")
                except:
                    num_of_stars    = None
                ##
                try:
                    num_of_stars    = container.find_element_by_css_selector(".stars-wrp meta").get_attribute("content") #y[0].get_attribute("content")
                except:
                    num_of_stars    = None
                ##
                try:
                    hotel_address = container.find_element_by_css_selector('[itemprop="address"]').text
                except:
                    hotel_address   = None
                ##
                ##
                try:
                    to_center = container.find_element_by_css_selector('[class="details-paragraph details-paragraph--location location-details"]').text
                except:
                    to_center   = None
                ##
                ##    Major Box items  ##
                try:
                    x = container.find_element_by_css_selector('[data-qa="price-per-stay"]').text #y[0].text
                    major_total_price = ''.join( c for c in x[2:] if c.isdigit() )
                except:
                    major_total_price     = None
                try:
                    x = container.find_element_by_css_selector('[data-qa="recommended-price"]').text #y[0].text
                    major_price_per_night = ''.join( c for c in x if c.isdigit() )
                except:
                    major_price_per_night     = None
                try:
                    major_seller   = container.find_element_by_css_selector('[data-qa="recommended-price-partner"]').text #y[0].text
                except:
                    major_seller   = None
                ##    end of Major Box  ##

                ##    Minor Box items  ##
                try:
                    x = container.find_element_by_class_name("accommodation-list__deal--c3f77").text #y[0].text
                    minor_price_per_night = ''.join( c for c in x if c.isdigit() )
                except:
                    try:
                        x   = container.find_element_by_xpath('//article[@data-co_li_lo="2"]').text #y[0].text
                        x = x.split('\n')[1]
                        minor_price_per_night = ''.join( c for c in x if c.isdigit() )
                    except:
                        minor_price_per_night   = None
                #calculate total minor price
                try:
                    x = container.find_element_by_css_selector('[class="accommodation-list__perStay--8526d"]').text
                    nights = int(x[:x.find("night")])
                    minor_total_price = nights*int(minor_price_per_night)
                except:
                    try:
                        x = container.find_element_by_css_selector('[data-qa="price-per-stay"]').text
                        nights = int(x[:x.find("night")])
                        minor_total_price = nights*int(minor_price_per_night)
                    except:
                        minor_total_price = None
                ##
                try:
                    minor_seller   = container.find_element_by_class_name("accommodation-list__heading--2bc8d").text #y[0].text
                except:
                    try:
                        x   = container.find_element_by_xpath('//article[@data-co_li_lo="2"]').text #y[0].text
                        minor_seller = x.split('\n')[0]
                    except:
                        minor_seller   = None

                ##    end of Minor Box  ##

                ##    Lowest Box items  ##
                try:
                    x = container.find_element_by_css_selector('[data-qa="cheapest-deal"]').text #y[0].text
                    lowest_price_per_night = ''.join(c for c in x if c.isdigit())
                except:
                    lowest_price_per_night     = None
                ##
                try:
                    lowest_seller   = container.find_element_by_class_name("accommodation-list__partner--5da6c").text #y[0].text
                except:
                    try:
                        lowest_seller   = container.find_element_by_class_name("accommodation-list__partner--58826").text #y[0].text
                    except:
                        try:
                            x = container.find_element_by_xpath('//button[@data-qa="cheapest-deal"]').text #y[0].text
                            lowest_seller = x.split('\n')[1]
                        except:
                            lowest_seller   = None
                ##    end of lowest Box  ##
                #Collecting items
                item['hotel_name'] = hotel_name
                item['hotel_link'] = hotel_link
                item['image_link'] = image_link
                item['rating'] = rating
                item['num_of_ratings'] = num_of_ratings
                item['num_of_stars'] = num_of_stars
                item['distance_to_city_center'] = to_center
                item['hotel_address'] = hotel_address
                item['major_total_price'] = major_total_price
                item['major_price_per_night'] = major_price_per_night
                item['major_seller'] = major_seller
                item['minor_price_per_night'] = minor_price_per_night
                item['minor_total_price'] = minor_total_price
                item['minor_seller'] = minor_seller
                item['lowest_price_per_night'] = lowest_price_per_night
                item['lowest_seller'] = lowest_seller
                yield(item)
            # Get the next page
            try:
                next_page = self.driver.find_element_by_class_name('btn.btn--pagination.btn--small.btn--page-arrow.btn--next')
                next_page.click()
                time.sleep(5)
            except:
                break
        self.driver.close()
        #To ensure that selenium web driver is closed
        try:
            self.driver.quit()
        except:
            pass
