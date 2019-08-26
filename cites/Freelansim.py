import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

class Freelansim:
    def __init__(self, url_main = 'https://freelansim.ru/tasks?_=1565689765433&page=', url_key = '&q=парсинг'):
        self.url_main = url_main
        self.url_key = url_key

    def all_pages(self):
        url = self.url_main+'1'+self.url_key
        
        headers = {"User-Agent":"Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')

        try:
            div = soup.find('div', class_ = 'pagination')
            a = div.find_all('a')
            u = []
            for i in a:
                try:
                    i = int(i)
                    u.append(i)
                except:
                    pass
            return max(u)
        except:
            return 1

    def parse(self, keys):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            url = self.url_main+str(j)+self.url_key

            headers = {"User-Agent":"Mozilla/5.0"}
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')

            div = soup.find_all('div', class_ = 'task__title')
            times = soup.find_all('span', class_ = 'params__published-at icon_task_publish_at')
            k = 0
            for name in div:
                time = times[k].text
                k += 1
                link = 'https://freelansim.ru' + name.find('a').get('href')
                name = name.get('title')
                try:
                    name = ''.join(name.split('\\'))
                except:
                    pass
                orders[(name,time)] = link
        return orders