import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

from cites.Weblancer import Weblancer
from cites.Freelansim import Freelansim
from cites.Kwork import Kwork

# вместо этого можно будет просто искать подстроки парс и pars в словах
keys = ['парсинг', 'спарсить', 'парсер',
        'Парсинг', 'Спарсить', 'Парсер',
        'ПАРСИНГ', 'СПАРСИТЬ', 'ПАРСЕР',
        'parser','parsing','parse',
        'Parser','Parsing','Parse',
        'PARSER','PARSING','PARSE']

def main():
    with open('List.txt', 'a') as List:
        List.write(str(datetime.now())+'\n')
    List.close()
    
    previous_orders = []
    with open('List.txt', 'r') as List:
        for order in List:
            previous_orders.append(order)
    List.close()

    orders = {**Weblancer().parse(keys), **Freelansim().parse(keys), **Kwork().parse(keys)}

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
