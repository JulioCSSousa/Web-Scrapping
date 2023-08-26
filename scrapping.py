import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math


url = 'https://www.kabum.com.br/gamer/acessorios-gamer/joystick?page_number=2&page_size=20&facet_filters=&sort=most_searched'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('div', id='listingCount').get_text().strip()

print(qtd_itens)

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]

last_pag = math.ceil(int(qtd)/20)

dict_products = {'marca':[], 'preco':[]}

for i in range(1, last_pag+1):
    url_pag = f'https://www.kabum.com.br/gamer/acessorios-gamer/joystick?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    products = soup.find_all('div',class_=re.compile('productCard'))

    for product in products:
        marca = product.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = product.find('span', class_=re.compile('priceCard')).get_text().strip()

        print(marca, preco)

        dict_products['marca'].append(marca)
        dict_products['preco'].append(preco)

    print(url_pag)

df = pd.DataFrame(dict_products)
df.to_csv('C:/Users/julio/Desktop/eight_bit_Do-JoystickPrices.csv', encoding='utf-8', sep=';')

