from bs4 import BeautifulSoup
from selenium import webdriver
from colors import bcolors
import json
import time
import warnings
from selenium.webdriver.common.keys import Keys
import os

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

    def find_article(self, titles):
        self.login()
        articles_ids = []
        print( str(len(titles)) +  " torizon articles found ✅")
        for element in titles:
            time.sleep(1)
            self.driver.get("https://developer1.toradex.com/acp/content/post/")
            try:
                self.driver.find_element_by_name("PostSearch[name]").send_keys(element + Keys.ENTER)
            except:
                print(element + " : error on the search")
            try:
                time.sleep(2)
                self.driver.find_element_by_xpath("//tr[@class='grid']//a[@title='"+element+"']").click()
                page_textbox = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
                currentURL = self.driver.current_url
                id = currentURL[-6:]
                articles_ids.append(id)
                print(articles_ids)
            except:
                pass

        return articles_ids

    def DeveloperBot(self, articles_ids):
        self.driver.get("https://developer1.toradex.com/acp/content/post/update?id=103348") ## torizon documentation page
        content = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
        html = content.get_attribute("innerHTML")
        articles_str = ""
        for id in articles_ids:
            if id in html:
                print(id + bcolors.OKGREEN + ": OK" + bcolors.ENDC)
                articles_str+= id + ": OK" + "\n"
            else:
                self.driver.get("https://developer1.toradex.com/acp/content/post/update?id="+ str(id))
                title = self.driver.find_element_by_tag_name("small")
                print(id + bcolors.WARNING + " " + title.text + ": No" + bcolors.ENDC)
                articles_str+= id + " " + title.text + " :No" + "\n"
        
        time.sleep(5)
        opt = True
        while(opt):
            opt = str(input("Do you want to save logs? y/n:"))
            if opt == "y":
                file_name = input("Name for the log: ")
                f = open("logs/"+file_name+".txt", "w")
                f.write(articles_str)
                f.close()
                print(file_name + " created!")
                os.system('tree -t')
                opt = None
                self.driver.close()
            elif opt == 'n':
                opt =  None
                print("bye")
                self.driver.close()
            else:
                print("wrong option")
    

if __name__ == "__main__":
    bot = bot()
    titles = bot.TorizonNewArticles()
    articles_ids = bot.find_article(titles)
    bot.DeveloperBot(articles_ids)





    