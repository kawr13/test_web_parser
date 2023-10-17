# Асинхронный веб-скраппер для извлечения данных с веб-страниц

import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

# Функция для получения HTML-кода страницы
async def srappers(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

# Функция для извлечения ссылок на статьи с веб-страницы
async def soup_text(sites: str):
    soup = bs(sites, 'lxml')
    url_detailed = soup.select('a.tm-title__link')
    data = [f"https://habr.com{url.get('href')}" for url in url_detailed]
    return data

# Функция для получения данных со страницы статьи
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

# Функция для обработки каждой страницы статьи
async def process_page(url):
    data = await fetch_data(url)
    soup = bs(data, 'lxml')
    words = soup.select_one('div.tm-article-presenter')
    header = words.find('h1').text
    text = [i.text for i in soup.select('p')]
    dat_parse = {'header': header, 'text': text}
    return dat_parse

# Основная функция для выполнения всего процесса
async def main(url: str):
    sites_dat = []
    sites_data = await srappers(url)
    data = await soup_text(sites_data)
    coros = [process_page(i) for i in data]
    results = await asyncio.gather(*coros)
    sites_dat.extend(results)
    return sites_dat

if __name__ == "__main__":
    answ = 'python'
    URL = rf'https://habr.com/ru/search/?q={answ}&target_type=posts&order=relevance'
    date = asyncio.run(main(URL))
    print(date)