import requests
from bs4 import BeautifulSoup
from time import sleep
import gspread
from datetime import date

starting_url = 'https://www.ebay.com.au/sch/i.html?_nkw=tempered+glass+protector&_sacat=0&_pgn=1'

def get_data(url):

    headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    r = requests.get(url=url, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract_store_info(soup):
    
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('scrapetosheets').sheet1

    products = soup.find_all('div', {'class': 's-item__info clearfix'})
    for product in products:
        try:
            title = product.find('h3', {'class':'s-item__title'}).text.strip()
        except:
            title = ''
        try:
            link = product.find('a', {'class':'s-item__link'})['href']
        except:
            link = ''
        try:
            price = product.find('span', {'class':'s-item__price'}).text.replace('AU $', '').strip()
        except:
            price = None
        try:
            product_info = product.find('span', {'class':'s-item__sme s-item__smeInfo'}).text.strip()
        except:
            product_info = ''
        try:
            brand = product.find('div', {'class':'s-item__subtitle'}).text.replace('Brand new', '').replace('· ', '').strip()
        except:
            brand = ''

        sh.append_row([title, link, price, product_info, brand])
      
    return

def get_nextpage(soup, current_url):
    if not current_url:
        return
    try:
        next_url = soup.find('a', {'class': 'pagination__next'})['href']
    except:
        next_url = None
        return
    if next_url == current_url:
        next_url = None
        return
    return next_url

url = starting_url
i = 1
while url and i < 5:
    print('extracting information from a new page')
    soup = get_data(url=url)
    extract_store_info(soup=soup)
    url = get_nextpage(soup=soup, current_url=url)
    i = i + 1
    sleep(5)



