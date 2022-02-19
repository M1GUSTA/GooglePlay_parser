import re
import time
import pandas as pd

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}


def get_source_html(url, last_point, num_file):
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe"
    )

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)
        i = 0
        while True:
            find_more_element = driver.find_element_by_class_name("RRKTjb")
            actions = ActionChains(driver)
            actions.move_to_element(find_more_element).perform()
            i += 1
            if i ==20:
                break
    except Exception as _ex:
        print(_ex)
    finally:
        if driver.find_element_by_id(last_point):
            with open("source-page.html", "w", encoding='utf-8') as file:
                file.write(driver.page_source)
        driver.close()
        driver.quit()
        get_items_urls(file_path="C:\\Users\\HP\\Desktop\\Scrapping\\google_play\\source-page.html")
        get_data(file_path="C:\\Users\\HP\\Desktop\\Scrapping\\google_play\\item_urls.txt", num_file=num_file)

def get_items_urls(file_path):
    with open(file_path, encoding='utf-8') as file:
        src = file.read()


    soup = BeautifulSoup(src, 'lxml')
    items_div = soup.find_all("div", class_="wXUyZd")
    print(items_div)

    urls = []
    for item in items_div:
        item_url = item.find("a").get("href")
        urls.append(item_url)

    with open("item_urls.txt", "w") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"

def get_data(file_path, num_file):
    with open(file_path, encoding='utf-8') as file:
        urls_list = [url.strip() for url in file.readlines()]
    data = []

    for url in urls_list:
        response = requests.get(url=f"https://play.google.com{url}", headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        print(response)
        url_app=f"https://play.google.com{url}"

        try:
            title = soup.find('h1', class_="AHFaub").find("span").text.strip()
        except Exception as _ex:
            title = None

        #Разработчик
        try:
            developer = soup.find('span', class_="T32cc").find('a').string
        except Exception as _ex:
            developer = None

        #Разработчик
        try:
            price = soup.find('span', class_="oocvOe").find('button').text.strip()
        except Exception as _ex:
            price = None

        #Категория
        try:
            genre = soup.find('a', {"itemprop": "genre"}).string
        except Exception as _ex:
            genre = None

        # Рейтинг
        try:
            rating = soup.find('div', class_="BHMmbe").string
        except Exception as _ex:
            rating = None

        # Отзывы
        try:
            rate_count = soup.find('span', class_="AYi5wd").find("span").string
        except Exception as _ex:
            rate_count = None

        # Установки
        try:
            download_count = soup.find_all('div', class_="hAyfc")[2].find("span", class_="htlgb").string
        except Exception as _ex:
            download_count = None

        # Цена
        try:
            paid_content = soup.find_all('div', class_="hAyfc")[6].find("span", class_="htlgb").string
        except Exception as _ex:
            paid_content = None

        # Адрес разработчика
        try:
            dev_adress = soup.find_all('div', class_="hAyfc")[-1].find("span", class_="htlgb").find_all("div")[-1].string
            dev_adress = re.sub("^\s+|\n|\r|\s+$", '', dev_adress)
        except Exception as _ex:
            dev_adress = None

        # email разработчика
        try:
            dev_email = soup.find_all('div', class_="hAyfc")[-1].find("span", class_="htlgb").find_all("div")[2].find("a").string
        except Exception as _ex:
            dev_email = None

        # размер
        try:
            weight = soup.find_all('div', class_="hAyfc")[1].find("span", class_="htlgb").string
        except Exception as _ex:
            weight = None

        # Версия
        try:
            version = soup.find_all('div', class_="hAyfc")[4].find("span", class_="htlgb").string
        except Exception as _ex:
            version = None

        # Дата обновления
        try:
            update_date = soup.find_all('div', class_="hAyfc")[0].find("span", class_="htlgb").string
        except Exception as _ex:
            update_date = None

        # try:
        #         driver = webdriver.Chrome(
        #             executable_path="chromedriver.exe"
        #         )
        #         driver.maximize_window()
        #         driver.get(url=f"{url_app}&showAllReviews=true")
        #         while True:
        #             find_more_element = driver.find_element_by_class_name("CwaK9")
        #             actions = ActionChains(driver)
        #             actions.move_to_element(find_more_element).perform()
        #             time.sleep(1)
        #             if driver.find_element_by_class_name("CwaK9"):
        #                 continue
        #             else:
        #                 with open("comments.html", "w", encoding='utf-8') as file:
        #                     file.write(driver.page_source)
        #



        except Exception as _ex:
            create_date = None

        print(title)
        print(price)

        columns=["Название", "Разработчик", "Категория", "Цена", "Рейтниг", "Отзывы",
                 "Установки", "Адрес разработчика", "Email разработчика", "Размер",
                 "Требуемая версия Android", "Дата публикации", "Дата обновления", "url"]

        data.append([title, developer, genre, price, rating, rate_count, download_count,
                     dev_adress, dev_email, weight, version, "", update_date, url_app])

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(rf'data_file{num_file}.csv', encoding="utf-8")

def main():
    get_source_html(url="https://play.google.com/store/search?q=%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8%20pro&c=apps", last_point="c199", num_file=1)
    get_source_html(url="https://play.google.com/store/search?q=%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8&c=apps", last_point="c199", num_file=2)
    get_source_html(url="https://play.google.com/store/search?q=%D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81&c=apps", last_point="c199", num_file=3)


if __name__ == "__main__":
    main()