import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

keys = ['парсинг', 'спарсить', 'парсер',
        'Парсинг', 'Спарсить', 'Парсер',
        'ПАРСИНГ', 'СПАРСИТЬ', 'ПАРСЕР',
        'parser','parsing','parse',
        'Parser','Parsing','Parse',
        'PARSER','PARSING','PARSE']

def make_soup(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup



class Weblancer:
    def __init__(self, url = 'https://www.weblancer.net/jobs/?action=search&keywords=%EF%E0%F0%F1%E8%ED%E3'):
       self.url = url
    
    def all_pages(self):
        soup = make_soup(self.url)
        try:
            div = soup.find('div', class_ = 'col-1 col-sm-2 text-right')
            link = div.find('a').get('href')
            pages = int(str(link).split('=')[5])
        except:
            pages = 1
        return pages

    def parse(self):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            if j != 1:
                url = self.url + '&page=' + str(j)
            else:
                url = self.url
            soup = make_soup(url)
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




class Freelansim:
    def __init__(self, url_main = 'https://freelansim.ru/tasks?_=1565689765433&page=', url_key = '&q=парсинг'):
        self.url_main = url_main
        self.url_key = url_key

    def all_pages(self):
        url = self.url_main+'1'+self.url_key
        soup = make_soup(url)
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

    def parse(self):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            url = self.url_main+str(j)+self.url_key
            soup = make_soup(url)
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




class Kwork:
    def __init__(self, url = 'https://kwork.ru/projects?page='):
        self.url = url

    def all_pages(self):
        soup = make_soup(self.url+'1')
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

    def parse(self):
        orders = {}
        j = 0
        while j < self.all_pages():
            j += 1
            url = self.url + str(j)
            soup = make_soup(url)
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


def main():
    with open('List.txt', 'a') as List:
        List.write(str(datetime.now())+'\n')
    List.close()
    
    previous_orders = []
    with open('List.txt', 'r') as List:
        for order in List:
            previous_orders.append(order)
    List.close()

    orders = {**Weblancer().parse(), **Freelansim().parse(), **Kwork().parse()}

    i = 0
    with open('List.txt', 'a') as List:
        for x in orders:
            if orders[x]+'\n' not in previous_orders:
                List.write(orders[x]+'\n')
                i += 1
                print(x[0])
                print(x[1])
                print(orders[x],'\n')

    List.close()

    if i == 0:
        print('Новых заказов нет')


if __name__ == "__main__":
    main()

    input('')
