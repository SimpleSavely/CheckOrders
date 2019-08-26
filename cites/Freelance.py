import requests, time
from bs4 import BeautifulSoup
from datetime import datetime


class Freelance:
    def __init__(self, url = 'https://freelance.ru/projects/filter/?specs=4:133:116:673:117&page='):
       self.url = url

    def all_pages(self):

        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(self.url+'1', headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        
        ul = soup.find('ul', class_ = 'pagination pagination-default')
        lis = ul.find_all('li')
        L = []
        for li in lis:
            try:
                li = int(li.text)
                L.append(li)
            except:
                pass
        return max(L)

    def parse(self, keys):
        print('Freelance.ru')
        orders = {}
        j = 0
        pages = self.all_pages()
        while j < pages:
            j += 1
            print(str(round((j/pages)*100))+'%')

            headers = {"User-Agent":"Mozilla/5.0"}
            html = requests.get(self.url+str(j), headers=headers).text
            soup = BeautifulSoup(html, 'lxml')

            divs = soup.find_all('div', class_ = 'proj')
            for div in divs:
                name = div.find('h2').get('title')
                if name != 'Доступ для базовых аккаунтов закрыт заказчиком':
                    name = name.split(':')[0]
                    cost = div.find('span', class_ = 'cost').find('a').text
                    time_li = div.find('li', class_ = 'proj-inf pdata pull-left').text
                    time_m = time_li.split(' ')
                    link = 'https://freelance.ru' + div.find('a', class_ = 'ptitle').get('href')
                    if len(time_m) == 2:
                        time = time_m[1]
                    else:
                        time = time_m[0]
                words = name.split(' ')
                for word in words:
                    if word in keys:
                        orders[(name,time)] = link
        return orders