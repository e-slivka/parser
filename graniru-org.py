import json
import requests
from bs4 import BeautifulSoup

url = 'https://graniru.org/'


def get_page_content(link, image):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    new_title = soup.h3.text

    body_news = soup.find("div", class_="main-text")
    body_news = body_news.text.strip()

    date_news = soup.find("span", class_="date")
    date_news = date_news.text[6:]+'.' + \
        date_news.text[3:5]+'.'+date_news.text[0:2]

    page_info = {
        "url": link,
        "img": image,
        "title": new_title,
        "body": body_news,
        "date": date_news
    }

    return page_info


# список ссылок всех новостей сайта
def get_links():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    url_n = soup.find_all("div", class_="row fp-blk fp-blk-1")
    url_news = []
    for item in url_n:
        # print("https://graniru.org" + item.a['href'])
        url_news.append("https://graniru.org" + item.a['href'])
    return url_news


# список всех картинок в новостях сайта
def img():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    img_news = []
    for link in soup.find_all('img', class_="card-img-top"):
        img_news.append("https://graniru.org"+link.get('src'))
    return img_news


def main():
    links = get_links()
    news_img = img()
    links = zip(links, news_img)
    top_news = []
    for link, image in links:
        print(f"Обрабатывается {link}")
        info = get_page_content(link, image)
        top_news.append(info)

    with open("news-graniru-org.json", "wt") as f:
        json.dump(top_news, f)
    print("Работа завершена")


# Главная функция
if __name__ == "__main__":
    main()
