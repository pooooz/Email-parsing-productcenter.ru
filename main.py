import requests
from bs4 import BeautifulSoup
import csv

URL = "https://productcenter.ru/producers/catalog-produkty-pitaniia-45"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
names = []
FILE = 'info.csv'


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    count = soup.find('div', class_='page_links').findAll('a')[-2].text
    return int(count)


def get_email(link):
    temp_soup = BeautifulSoup(get_html(link).text, 'html.parser')
    email = temp_soup.find('div', class_='bc_text').find('span', itemprop='email').text
    return email


def save_file(info, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Email'])
        for item in info:
            writer.writerow([item['name'], item['link'], item['email']])
    file.close()


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    item_group = soup.findAll('div', class_='item_body')
    for item in item_group:
        link = 'https://productcenter.ru' + item.find('a', class_='link').get('href')
        names.append({
            'name': item.find('a', class_='link').text,
            'link': link,
            'email': get_email(link)})


def parse():
    html = get_html(URL).text
    pages_count = get_pages_count(html)
    print(f'Парсинг страницы 1 из {pages_count}...')
    get_content(html)
    for page in range(1, pages_count + 1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        html = get_html(URL + f'/page-{page}').text
        get_content(html)

    save_file(names, FILE)


if __name__ == "__main__":
    parse()
