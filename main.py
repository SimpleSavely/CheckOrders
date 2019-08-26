import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

import tkinter as tk

from cites.Weblancer import Weblancer
from cites.Freelansim import Freelansim
from cites.Kwork import Kwork
from cites.Freelance import Freelance

# class Main(tk.Frame):
#     def __init__(self, root):
#         super().__init__(root)
#         self.init_main()

#     def init_main(self):
#         menu = tk.Menu(root)
#         root.config(menu=menu)

#         settingsmenu = tk.Menu(menu)
#         settingsmenu.add_command(label='Список сайтов для поиска',
#                                  command=self.open_cites_list)
#         settingsmenu.add_command(label='Список ключевых слов',
#                                  command=self.open_keys_list)

#         menu.add_command(label='Обновить', command=self.update_orders())
#         menu.add_cascade(label='Настройки', menu=settingsmenu)

    
#     def update_orders(self):
#         # надо как-то спарсить и вывести информацию о заказах
#         # и сохранить ее
#         pass

#     def open_cites_list(self):
#         CitesList(root)

#     def open_keys_list(self):
#         KeysList(root)



# class CitesList(tk.Toplevel):
#     def __init__(self,root):
#         super().__init__(root)
#         self.init_cites_list()

#     def init_cites_list(self):
#         self.title('Список сайтов для поиска')
#         self.geometry('400x320+400+300')
#         self.resizable(False, False)

#         self.grab_set()
#         self.focus_set()

#         self.check_buttons = []
#         cites = ['Weblancer', 'Freelansim', 'Kwork']
#         for cite in cites:
#             self.check_buttons.append(tk.Checkbutton(self,text=cite))
#         for check_button in self.check_buttons:
#             check_button.pack()

#         self.okbutton = tk.Button(self, text='OK', command=self.save)
#         self.okbutton.pack()

#     def save(self):
#         # надо как-то сохранять список сайтов
#         self.destroy()

# class KeysList(tk.Toplevel):
#     def __init__(self,root):
#         super().__init__(root)
#         self.init_cites_list()

#     def init_cites_list(self):
#         self.title('Список ключевых слов')
#         self.geometry('400x200+400+300')
#         self.resizable(False, False)

#         self.grab_set()
#         self.focus_set()

#         label = tk.Label(self, text='Введите через запятую')
#         label.pack(side=tk.TOP)

#         okbutton = tk.Button(self, text='OK', command=self.save)
#         okbutton.pack(side=tk.BOTTOM)

#         text = tk.Text(self, width=45, height=10)
#         text.pack(side=tk.LEFT)

#         scroll = tk.Scrollbar(self, command=text.yview)
#         scroll.pack(side=tk.LEFT, fill=tk.Y)

#         text.config(yscrollcommand=scroll.set)

#     def save(self):
#         # надо как-то сохранять список сайтов
#         self.destroy()


# if __name__ == '__main__':
#     root = tk.Tk()
#     app = Main(root)
#     app.pack()
#     root.title('Дайтеденяк')
#     root.geometry('650x450+300+200')
#     root.resizable(False, False)

#     root.mainloop()

########################################################################

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

    orders = {**Weblancer().parse(keys), **Freelansim().parse(keys), **Kwork().parse(keys), **Freelance().parse(keys)}

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
    else:
        print('Найдено',len(orders),'новых заказов')


if __name__ == "__main__":
    main()

    input('')