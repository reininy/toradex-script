from bs4 import BeautifulSoup
from selenium import webdriver
from colors import bcolors
import json
import time
import warnings

class bot():
    warnings.filterwarnings('ignore')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    file =  open('settings.json', 'r')
    data = json.load(file)
    final_data = data['settings']

    def login(self):
        self.driver.get("https://developer1.toradex.com/acp/default/login")
        self.driver.find_element_by_name('LoginForm[username]').send_keys(self.final_data['username'])
        self.driver.find_element_by_name('LoginForm[password]').send_keys(self.final_data['password'])
        self.driver.find_element_by_name('login-button').click()

    def TorizonNewArticles(self):
        self.driver.get("https://developer.toradex.com/knowledge-base?tags=101691&cond=and")
        content = self.driver.find_element_by_class_name('result-tags')
        html = content.get_attribute("innerHTML")
        soup= BeautifulSoup(html , 'html.parser')
        titles = [p.text for p in soup.findAll('li')]
        
        return titles


    def DeveloperBot(self, titles):
        self.login()
        self.driver.get("https://developer1.toradex.com/acp/content/post/update?id=103348")
        content = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
        html = content.get_attribute("innerHTML")
        
        for title in titles:
            if title in html:
                print(title + bcolors.OKGREEN + ": OK" + bcolors.ENDC)
            else:
                print(title + bcolors.WARNING + ": No" + bcolors.ENDC)
            

        time.sleep(10)
        self.driver.close()
    

if __name__ == "__main__":
    bot = bot()
    titles = bot.TorizonNewArticles()
    bot.DeveloperBot(titles)





    