import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

class Weblancer:
    def __init__(self, url = 'https://www.weblancer.net/jobs/?action=search&keywords=%EF%E0%F0%F1%E8%ED%E3'):
       self.url = url
    
    def make_soup(url):
        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        return soup
    
    def all_pages(self):

        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(self.url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')

        try:
            div = soup.find('div', class_ = 'col-1 col-sm-2 text-right')
            link = div.find('a').get('href')
            pages = int(str(link).split('=')[5])
        except:
            pages = 1
        return pages

    def parse(self, keys):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            if j != 1:
                url = self.url + '&page=' + str(j)
            else:
                url = self.url
            
            headers = {"User-Agent":"Mozilla/5.0"}
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            
            names = soup.find_all('a', class_ = 'text-bold show_visited')
            times_ago = soup.find_all('span', class_ = 'time_ago')
            k = 0
            for name in names:
                time_ago = times_ago[k].text
                k += 1
                link = 'https://www.weblancer.net' + str(name.get('href'))
                name = name.text
                try:
                    name = ''.join(name.split('\\'))
                except:
                    pass
                orders[(name,time_ago)] = link
        return orders