from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd


class SacombankCrawler:
    def __init__(self) -> None:
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1920,1080")
        self.error = []
        self.metadata_ids = 0
        self.ids = 10

    def save_to_jsonl(self, filename, list_file) -> None:
        path = f'data/json/{filename}.jsonl'
        with open(path, 'w', encoding='utf8') as f:
            for conv in list_file:
                json_str = json.dumps(conv, ensure_ascii=False)
                f.write(json_str+'\n')
            
            
    def get_section(self, url):
        self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(2)
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".nav-product [href]")
        type_links = [element.get_attribute('href') for element in elements]
        type_names = [element.text for element in elements]
        self.browser.quit()
        return dict(zip(type_names,type_links))  
        
        
    def get_news(self, url="https://www.sacombank.com.vn/company/Pages/Tin-sacombank.aspx") -> None:
        news_dict = {'title': [], 'date': [], 'sources': []}
        news_list = []
        self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)
        sleep(2)
        elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [href]")
        links = [element.get_attribute('href') for element in elements]
        news_dict['sources'] = [*set(links)]        
        self.browser.quit()
        for news_link in news_dict['sources']:
            self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(news_link)
            sleep(2)
            element_1 = self.browser.find_element(By.CSS_SELECTOR, ".block-newdetail h1")
            news_dict['title'].append(element_1.text)            
            element_2 = self.browser.find_element(By.CSS_SELECTOR, ".block-newdetail div")
            news_list.append({'prompt': element_1.text, 'response':element_2.text})
            element_2 = self.browser.find_element(By.CSS_SELECTOR, ".block-newdetail time")
            news_dict['date'].append(element_2.text)
            self.browser.quit()
        self.save_to_jsonl(filename='news.jsonl', list_file=news_list)
        pd.DataFrame.from_dict(news_dict).to_csv('data/news.csv')


    # def get_InternetBanking_details(self):
    #     details = []
    #     df = pd.read_csv('data/metadata_internet_banking.csv', sep=',')    
    #     for row in df.values:        
    #         self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
    #         self.browser.get(row[-1])
    #         sleep(2)
    #         try:
    #             element = self.browser.find_element(By.XPATH, "/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[1]/div/div/div/div/h3")
    #             name = element.text
    #             # print(1)
    #         except:
    #             # print(2)
    #             self.browser.quit()
    #             continue            
    #         for i in range(2, 30):
    #             try:
    #                 content_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")
    #                 title_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[1]/h3")
    #                 details.append({"prompt":f"{row[1]}: {title_element.text} {name}", "response":content_element.text})
    #                 # print(3)
    #             except:
    #                 # print(4)
    #                 self.browser.quit()
    #                 break            
    #         self.browser.quit()   
    #     self.save_to_jsonl(filename='internet_banking_details.jsonl', list_file=details)

    # def get_save_details(self):
    #     details = []
    #     df = pd.read_csv('data/metadata_save.csv', sep=',')    
    #     for row in df.values:        
    #         self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
    #         self.browser.get(row[-1])
    #         sleep(2)
    #         try:
    #             element = self.browser.find_element(By.XPATH, "/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[1]/div/div/div/div/h3")
    #             name = element.text
    #         except:
    #             self.browser.quit()
    #             continue
    #         for i in range(2, 30):
    #             try:
    #                 content_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")                    
    #                 title_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[1]/h3")
    #                 details.append({"prompt":f"{title_element.text} {name}", "response":content_element.text})
    #             except:
    #                 try:
    #                     print(4)
    #                 except:
    #                     self.browser.quit()
    #                     break            
    #         self.browser.quit()         
    #     self.save_to_jsonl(filename='save_details.jsonl', list_file=details)
    
    
    def get_metadata(self, url="https://www.sacombank.com.vn/canhan/Pages/Bao-hiem.aspx"):
        metadata = {'sections':[],'subsections': [], 'sources': []}
        section = self.get_section(url)
        
        for name in section:
            link = section[name]
            self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(url=link)
            sleep(2)
            try:
                elements = self.browser.find_elements(By.CSS_SELECTOR, ".item [href]")
                for element in elements:
                    if element.get_attribute('href') not in metadata['sources']:
                        metadata['sources'].append(element.get_attribute('href'))
                elements = self.browser.find_elements(By.CSS_SELECTOR, ".item h4")
                for element in elements:
                    metadata['subsections'].append(element.text)                        
                    metadata['sections'].append(name)
                self.browser.quit()
            except:
                self.browser.quit()
                self.error.append(link)
                print("crawling error at ", link)
        try: 
            pd.DataFrame.from_dict(metadata).to_csv(f'data/metadata_{self.ids}.csv')
            self.ids+=1
        except:
            print("save metadata failed")

    def get_details(self, filename):
        details = []        
        df = pd.read_csv(f'data/meta/{filename}.csv', sep=',')        
        for row in df.values:
            # row = [, sections, subsections, sources]
            self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
            self.browser.get(row[-1])
            sleep(2)
            try:
                element = self.browser.find_element(By.XPATH, "/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[1]/div/div/div/div/h3")
                name = element.text                
            except:
                try:
                    element = self.browser.find_element(By.XPATH, "/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[1]/div/div/div/div/h3")
                    name = element.text
                except:                                        
                    self.browser.quit()
                    self.get_metadata(row[-1])                    
                    continue                                                                        
            for i in range(2, 30):
                try:
                    content_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")                    
                    title_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[1]/h3")
                    details.append({"prompt":f"{title_element.text} {name}", "response":content_element.text})
                except:
                    try:
                        content_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[2]")
                        title_element = self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[3]/div/div[3]/div[1]/div[2]/section[{i}]/div/div/div[1]/h3")
                        details.append({"prompt":f"{title_element.text} {name}", "response":content_element.text})                        
                    except:
                        self.browser.quit()
                        break            
            self.browser.quit()         
        self.save_to_jsonl(filename=f'details_{self.ids*10}', list_file=details)
        self.ids+=1
    
    def get_FAQs(self, url='https://www.sacombank.com.vn/canhan/Pages/cau-hoi-thuong-gap.aspx'):
        Sacombank_FAQs = []
        self.browser = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.browser.get(url)        
        sleep(2)                     
        # self.browser.execute_script("document.body.style.zoom='50%'")                      
        for i in range(1,101):
            try:
                element_q= self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[2]/div/div/div/div[1]/section/div/div/div[1]/div/div[4]/div[1]/div[{i}]/div[1]")
                element_a= self.browser.find_element(By.XPATH, f"/html/body/form/div[11]/div[3]/div[2]/main/div[4]/div/div[3]/div[2]/div/div/div/div[1]/section/div/div/div[1]/div/div[4]/div[1]/div[{i}]/div[2]")
                self.browser.execute_script("arguments[0].setAttribute('style','display:block;');", element_a)
                sleep(2)
                response = element_a.text
                prompt = element_q.text
                Sacombank_FAQs.append({'prompt':prompt, 'response':response})
                if i % 10 == 0:                    
                    self.browser.find_element(By.XPATH, "//a[@onclick=\"NextFAQ();\"]").click()                                
                    sleep(2)
            except:
                break
        self.browser.quit()
        self.save_to_jsonl(filename=f'Sacombank_FAQs', list_file=Sacombank_FAQs)
        
        
    def get(self, ):
        pass


if __name__ == '__main__':
    crawl = SacombankCrawler()
    # crawl.get_FAQs()
    # # crawl.get_metadata()
    # metadata = [f'metadata_{i}' for i in range(0,7)]    
    # for filename in metadata:
        # crawl.get_details(filename=filename)    