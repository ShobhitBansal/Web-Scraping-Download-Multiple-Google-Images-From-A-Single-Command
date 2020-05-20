# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from scrapy.loader import ItemLoader
from google_images.items import GoogleImagesItem
from scrapy.exceptions import CloseSpider

class DownloadSpider(scrapy.Spider):
    name = 'download'
    allowed_domains = ['www.google.co.in/imghp?hl=en']
    start_urls = ['https://www.google.co.in/imghp?hl=en']



    def __init__(self, searchword="", no_of_images=50):
        if searchword=="":
            raise CloseSpider('No SearchWord Entered')

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.set_window_size(1920,1080)
        driver.get("https://www.google.co.in/imghp?hl=en")

        search_box = driver.find_element_by_xpath("//input[@title='Search']")
        search_box.send_keys(searchword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            for i in range(6):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            btn = driver.find_element_by_xpath("//input[@value='Show more results']")
            btn.click()

            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            imgs = driver.find_element_by_xpath("//div[@id='islrg']/div/div/a[1]")
            self.html = []
            self.no_of_images = int(no_of_images)
            total_images = int(1.1*self.no_of_images)
            for i in range(total_images):
                try:
                    imgs = driver.find_element_by_xpath("//div[@id='islrg']/div/div[{0}]/a[1]".format(i+2))
                    imgs.click()
                    time.sleep(3)
                    self.html.append(driver.page_source)
                except:
                    continue

        except:
            raise CloseSpider('No Images Found for the entered searchword')
            
        driver.close()

    def parse(self, response):
        counter = 0
        for body in self.html:
            
            if counter>=self.no_of_images:
                break
            resp = Selector(text=body)
            loader = ItemLoader(item=GoogleImagesItem())
            url = resp.xpath("//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img/@src").get()
            name = resp.xpath("//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img/@alt").get()
            if "https" in url:
                loader.add_value('image_urls', url)
                loader.add_value('image_name',name)

                yield loader.load_item()
                counter+=1