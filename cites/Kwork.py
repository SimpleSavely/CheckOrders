import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

class Kwork:
    def __init__(self, url = 'https://kwork.ru/projects?page='):
        self.url = url

    def make_soup(url):
        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def all_pages(self):

        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(self.url+'1', headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        
        p = soup.find('div', class_ = 'p1')
        smth = p.find_all('a')
        pp = []
        for useness in smth:
            link = useness.get('href')
            pages = useness.text
            try:
                pages = int(pages)
                pp.append(pages)
            except:
                pass
        return max(pp)

    def parse(self, keys):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            url = self.url + str(j)

            headers = {"User-Agent":"Mozilla/5.0"}
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')

            div = soup.find_all('div', class_ = 'wants-card__header-title first-letter breakwords')
            times = soup.find_all('div', class_ = 'query-item__info mb10 ta-left')
            k = 0
            for d in div:
                time = ' '.join(times[k].text.split(' ')[:5])
                k += 1
                link = d.find('a').get('href')
                name = d.text
                try:
                    name = ''.join(name.split('\\'))
                except:
                    pass
                words = name.split(' ')
                for word in words:
                    if word in keys:
                        orders[(name,time)] = link
        return orders