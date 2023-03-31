from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

class SacombankCrawler:
    def __init__(self) -> None:
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1920,1080")
        self.news_dict = {'title': [], 'content': [], 'date': [], 'sources': []}
        self.card_dict = {'types':[],'names': [], 'images': [], 'sources': []}
        self.card_details = {}


    def get_news(self, url="https://www.sacombank.com.vn/company/Pages/Tin-sacombank.aspx"):
        self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(2)
        try:
            elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [href]")
            links = [element.get_attribute('href') for element in elements]
            self.news_dict['sources'] = [*set(links)]
            elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [img]")
            self.news_dict['images'] = [element.get_attribute('src') for element in elements]
        finally:
            self.browser.quit()
            
        for news_link in self.news_dict['sources']:
            self.browser = webdriver.Chrome(
                options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(news_link)
            sleep(2)
            try:
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail h1")
                self.news_dict['title'].append(element.text)
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail time")
                self.news_dict['date'].append(element.text)
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail div")
                self.news_dict['content'].append(element.text)
            finally:
                self.browser.quit()


    def get_card(self, url="https://www.sacombank.com.vn/canhan/Pages/The-tin-dung-2112010000.aspx"):
        self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(2)
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".nav-product [href]")        
        type_links = [element.get_attribute('href') for element in elements]
        type_names = [element.text for element in elements]
        types = dict(zip(type_names[0:5],type_links[0:5]))
        self.browser.quit()
        for type_name in types:
            self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(url=types[type_name])            
            sleep(2)
            elements = self.browser.find_elements(By.CSS_SELECTOR, ".item h4")
            for element in elements:
                self.card_dict['names'].append(element.text)
            
            elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [href]")
            for element in elements:
                if element.get_attribute('href') not in self.card_dict['sources']:
                    self.card_dict['sources'].append(element.get_attribute('href'))                
                        
            elements = self.browser.find_elements(By.CSS_SELECTOR, ".item img")
            for element in elements:
                self.card_dict['images'].append(element.get_attribute('src'))
            
            for element in range(len(elements)):
                self.card_dict['types'].append(type_name)
                
            self.browser.quit()
        pd.DataFrame.from_dict(self.card_dict).to_csv('data/card.csv')


    def  get_card_details(self):
        card_df = pd.read_csv('data/card.csv', sep=',')    
        for row in card_df.values:        
            self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(row[-1])
            sleep(2)
            title, content = [], []    
            element = self.browser.find_element(By.XPATH, "/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[1]/div/div/div/div/h3")
            name = element.text
            for i in range(2, 7):
                try:
                    content_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")
                    title_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[1]/h3")
                    title.append(title_element.text)
                    content.append(content_element.text)
                except:
                    self.browser.quit() 
                    break
            
            self.card_details[name] = dict(zip(title,content))
            self.browser.quit() 
        json_object = json.dumps(crawl.card_details, indent=4, ensure_ascii=False) 
        with open("data/card_details.json", "w",  encoding='utf8') as outfile:
            outfile.write(json_object)


if __name__ == '__main__':        
    crawl = SacombankCrawler()
    crawl.get_card()
    crawl.get_card_details()

