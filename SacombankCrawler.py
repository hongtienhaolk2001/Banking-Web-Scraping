from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options



class SacombankCrawler:
    def __init__(self) -> None:
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1080")
        self.news_dict = {'title': [],
                          'content': [], 'date': [], 'sources': []}
        self.credit_card_dict = {'names': [], 'images': [], 'benefits': [], 'limitation_and_fee': [],
                                 'requirements': [], 'register': [], 'sources': []}

    def get_news_links(self, url="https://www.sacombank.com.vn/company/Pages/Tin-sacombank.aspx"):
        self.browser = webdriver.Chrome(
            options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(5)
        try:
            elements = self.browser.find_elements(
                By.CSS_SELECTOR, ".item [href]")
            links = [element.get_attribute('href') for element in elements]
            self.news_dict['sources'] = [*set(links)]
            elements = self.browser.find_elements(
                By.CSS_SELECTOR, ".item [img]")
            self.news_dict['images'] = [
                element.get_attribute('src') for element in elements]
        finally:
            self.browser.quit()

    def get_credit_card_links(self, url="https://www.sacombank.com.vn/canhan/Pages/The-tin-dung-2112010000.aspx"):
        self.browser = webdriver.Chrome(
            options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(5)
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [href]")
        links = [element.get_attribute('href') for element in elements]
        self.credit_card_dict['sources'] = [*set(links)]
        sleep(2)
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".item h4")
        self.credit_card_dict['names'] = [element.text for element in elements]
        self.browser.quit()

    def get_credit_card_details(self):
        category = ['benefits', 'limitation_and_fee',
                    'requirements', 'register']
        for credit_card_link in self.credit_card_dict['sources']:
            self.browser = webdriver.Chrome(
                options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(credit_card_link)
            sleep(5)
            try:
                for i in range(2, 6):
                    element = self.browser.find_element(
                        By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")
                    sleep(2)
                    self.news_dict[category[i-2]].append(element.text)
            finally:
                self.browser.quit()

    def get_news_details(self):
        for news_link in self.news_dict['sources']:
            self.browser = webdriver.Chrome(
                options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(news_link)
            sleep(5)
            try:
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail h1")
                sleep(2)
                self.news_dict['title'].append(element.text)
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail time")
                sleep(2)
                self.news_dict['date'].append(element.text)
                element = self.browser.find_element(
                    By.CSS_SELECTOR, ".block-newdetail div")
                sleep(2)
                self.news_dict['content'].append(element.text)
            except:
                self.browser.quit()
            self.browser.quit()
