import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time
import random


# Формирование списка со ссылками на категории
def cat_links(url):
    links = [f'https://ofram.ru/good-category/{i}' for i in url]
    return links


# Основная функция сбора, структурирования и упаковки собранной информации в список
def parser_info(urls, headers):
    all_product = []

    for category in urls:
        req = requests.get(category, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        classes = ['col-md-6 col-lg-4', 'col-12 col-lg-6', 'col-md-4 col-lg-3', 'col-md-3']
        
        for class_ in classes:
            all_data = soup.find_all('div', {'class': class_})
            if all_data:
                for item in all_data:
                    product = []
                    link = item.find('a').get('href')

                    if link[len(link)-1:] == '/':
                        req2 = requests.get(link, headers=headers)
                        soup2 = BeautifulSoup(req2.text, 'lxml')

                        name = soup2.find(class_='door-cart-title').text
                        articul = soup2.find('span', class_='door-cart-attrs-title').text
                        price = soup2.find('h3', class_='price-new').text.lstrip()

                        product.append(name)
                        product.append(articul)
                        product.append(price)
                
                        all_product.append(product)
                        
                        pic_url = soup2.find_all('div', class_='door-item-gallery')

                        count = 0
                        for i in pic_url:
                            photo_list = i.find_all('img')
                            for item in photo_list:
                                photo_link = item.get('src')
                                if photo_link:
                                    picture = requests.get(photo_link)
                                    count += 1

                                    # Можно указать путь куда будет сохранён файл (через \\)
                                    # По умолчанию туда же, где исполняемый файл
                                    picture2 = open(f'{name}-{count}' + ".png", "wb") 
                                    picture2.write(picture.content)
                                    picture2.close()

                        time.sleep(random.randint(5, 30))

    return all_product


# Формирование файла CSV и запись в него информации
# Перед data можно указать путь куда будет сохранён файл (через \\).
# По умолчанию туда же, где исполняемый файл
def csv_writer(all_product):
    with open('data.csv', 'w',
              encoding='utf-8-sig', newline='') as file:        
        writer = csv.writer(file, delimiter=';')                
        writer.writerow(('наименование', 'артикул', 'цена'))
        
    for data in all_product:
        with open('data.csv', 'a',
                  encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)


# Заголовки и список категорий/подкатегорий
headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
           }

categories = [
    'mezhkomnatnye-dveri', 'protivopozharnye-dveri', 'zvukoizolyacionnye-dveri',
    'furnitura/?category_id=34', 'furnitura/?category_id=35',
    'plintus', 'mebel', 'boiserie'

    ]


if __name__=='__main__':
    urla = cat_links(categories)
    prod_info = parser_info(urla, headers)
    csv_creater = csv_writer(prod_info)




