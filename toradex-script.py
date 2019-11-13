from selenium import webdriver
from bs4 import BeautifulSoup as bd

import time

def dif(primeiro_arquivo, segundo_arquivo):
    arquivo = open(primeiro_arquivo, "r")
    arquivo2 = open(segundo_arquivo, "r")
    for line1 in arquivo:
        for line2 in arquivo2:
            if line1==line2:
                print("Same\n")
            else:
                print(line1 + line2)
                break
    arquivo.close()
    arquivo2.close()


def create_list(nome_arquivo, cont):
    arquivo = open(nome_arquivo, "w")
    arquivo.write(cont)
    arquivo.close()


driver = webdriver.PhantomJS() #colocando o path do driver do chrome

driver.get("https://developer.toradex.com/knowledge-base?tags=101691&cond=and")

time.sleep(2)
dados = driver.find_element_by_class_name("result-tags")
html = dados.get_attribute("innerHTML")
soup = bd(html, "html.parser")

cont = ""
for link in soup.find_all('a'):
    cont += str(link.get_text()+ "\n")

#print(cont)
driver.close()


# arquivo = open("lista.txt", "w")
# arquivo.write(cont)
# arquivo.close()

nome_arquivo = raw_input("Digite o nome do arquivo a ser criado:")
#print(nome_arquivo)

create_list(nome_arquivo, cont)


opt = raw_input("Deseja comparar a lista atual com a anterior?(sim ou nao)")
if(opt == 'sim'):
    segundo_arquivo = raw_input("Digite o nome:")
    #print(segundo_arquivo)
    dif(nome_arquivo, segundo_arquivo)
else:
    print("Lista atual gerada!")

# if(arquivo2 != NULL):
#     dif("lista.txt", "lista.txt")
# else:
#     print("Craw a list first")