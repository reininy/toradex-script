from bs4 import BeautifulSoup
from selenium import webdriver



def TorizonNewArticles():
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=D:\Python\Memory\WebWhatsAppBot")
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    url = 'https://developer.toradex.com/knowledge-base?tags=101691&cond=and'
    driver.get(url)
    content = driver.find_element_by_class_name('result-tags')
    html = content.get_attribute("innerHTML")
    soup= BeautifulSoup(html , 'html.parser')
    titles = [p.text for p in soup.findAll('li')]
    driver.close()

    return titles



def DeveloperBot(titles):
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=D:\Python\Memory\WebWhatsAppBot")
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    driver.get("https://developer1.toradex.com/acp/content/post/update?id=103348")

    content = driver.find_element_by_xpath('//*[@id="post-content_text"]')
    html = content.get_attribute("innerHTML")
    
    for title in titles:
        if title in html:
            print(title + ": OK")
        else:
            print(title + ": No")


if __name__ == "__main__":
    titles = TorizonNewArticles()
    #print(titles)
    DeveloperBot(titles)





    