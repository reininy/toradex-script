from bs4 import BeautifulSoup
from selenium import webdriver
from colors import bcolors
import json
import time
import warnings
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

class bot():
    PROGRAM_PATH = '/home/julio/projects/toradex-script/'
    warnings.filterwarnings('ignore')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(PROGRAM_PATH + 'chromedriver', chrome_options=options)
    file =  open('/home/julio/projects/toradex-script/settings.json', 'r')
    data = json.load(file)
    final_data = data['settings']

    def login(self):
        self.driver.get("https://developer1.toradex.com/acp/default/login")
        self.driver.find_element_by_name('LoginForm[username]').send_keys(self.final_data['username'])
        self.driver.find_element_by_name('LoginForm[password]').send_keys(self.final_data['password'])
        self.driver.find_element_by_name('login-button').click()

    def scrap(self, article_name):
        self.login()
        time.sleep(3)
        self.driver.get("https://developer1.toradex.com/acp/content/post/")
        self.driver.find_element_by_name("PostSearch[name]").send_keys(article_name + Keys.ENTER)
        currentURL = self.driver.current_url
        self.driver.get(currentURL)

        try:
            self.driver.find_element_by_xpath("//tr[@class='grid']//a[@title='"+article_name+"']").click()
            page_textbox = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
            page_text = page_textbox.text
            file = open(self.PROGRAM_PATH + '/articles/' + article_name + ".md", "w")
            file.write(page_text)
            file.close()
            
            print(bcolors.OKGREEN + "File downloaded" + bcolors.ENDC) 
            os.system('tree -t' +  self.PROGRAM_PATH + '/articles')

        except NoSuchElementException:
            #article_names = table.find_elements_by_xpath('//tr[@class="grid]')
            success = True
            print(bcolors.FAIL + "Article not found, did you mean?" + bcolors.ENDC)

            for name in self.driver.find_elements_by_xpath("//tr[@class='grid']"):
                text = name.find_element_by_tag_name('a').text
                print(bcolors.OKGREEN + text + bcolors.ENDC)

            while(success != None):
                print('entrando no while')
                article_name_retry = str(input('Please write one of the articles above:'))
                try: 
                    self.driver.find_element_by_xpath("//tr[@class='grid']//a[@title='"+article_name_retry+"']").click()
                    page_textbox = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
                    if (page_textbox != None): success = None
                except: pass
                    
            page_text = page_textbox.text
            file = open(self.PROGRAM_PATH + '/articles/' + article_name_retry + ".md", "w")
            file.write(page_text)
            file.close()
            print(bcolors.OKGREEN + "File downloaded" + bcolors.ENDC) 
            os.system('tree -t' +  self.PROGRAM_PATH + '/articles')

    def torizon_articles(self):
        self.driver.get("https://developer.toradex.com/knowledge-base?tags=101691&cond=and")
        content = self.driver.find_element_by_class_name('result-tags')
        html = content.get_attribute("innerHTML")
        soup= BeautifulSoup(html , 'html.parser')
        titles = [p.text for p in soup.findAll('li')]
        links  = soup.findAll('a')
        i = 0
        links_final = []
        for elem in links:
            if elem.get('href') is not None:
                if len(elem.get('href')) > 10:
                    i+=1
                    #print(elem.get('href'))
                    links_final.append('https://developer.toradex.com' + elem.get('href'))
            else:
                pass

        return titles, links_final

    def show_torizon_articles(self):
        titles, links = self.torizon_articles()
        print( str(len(titles)) +  " torizon articles found ✅")
        for elem, link in zip(titles, links):
            print(elem, link)

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

    def documentation_update(self, articles_ids):
        torizon_documentation = ['103953', '103952', '103951', '103950', '103349', '103703', '103954', '103940', '103941', '103942', '103943', '103944', '103945', '103946', '103947', '103948', '103949', '103955']
        torizon_documentation_merge = ''
        for id in torizon_documentation:
            self.driver.get('https://developer1.toradex.com/acp/content/post/update?id='+id)
            content = self.driver.find_element_by_xpath('//*[@id="post-content_text"]')
            html = content.get_attribute("innerHTML")
            torizon_documentation_merge+= html

        articles_str = "" # declare string to create text file
        for id in articles_ids:
            if id in torizon_documentation_merge:
                print(id + bcolors.OKGREEN + ": OK" + bcolors.ENDC)
                articles_str+= id + ": OK" + "\n"
            else:
                self.driver.get("https://developer1.toradex.com/acp/content/post/update?id="+ str(id))
                title = self.driver.find_element_by_tag_name("small")
                print(id + bcolors.WARNING + " " + title.text + ": No" + bcolors.ENDC)
                articles_str += id + " " + title.text + " :No" + "\n"
        
        time.sleep(5)
        opt = True
        while(opt):
            opt = str(input("Do you want to save logs? y/n:"))
            if opt == "y":
                file_name = input("Name for the log: ")
                f = open(self.PROGRAM_PATH + "/logs/"+file_name+".txt", "w")
                f.write(articles_str)
                f.close()
                print(file_name + " created!")
                os.system('tree -t ' +self.PROGRAM_PATH + '/logs/')
                opt = None
                self.driver.close()
            elif opt == 'n':
                opt =  None
                print("bye")
                self.driver.close()
            else:
                print("wrong option")
    






    
