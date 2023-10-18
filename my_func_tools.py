import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import aiofiles
from concurrent.futures import ThreadPoolExecutor


async def scrap(url: str):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

async def extract_urls(sites: str):
    soup = bs(sites, 'lxml')
    url_detailed = soup.find_all('a', class_='tm-title__link')
    data = [f"https://habr.com{url['href']}" for url in url_detailed]
    return data

async def fetch_data(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

async def process_page(url):
    data = await fetch_data(url)
    soup = bs(data, 'lxml')
    words = soup.find('div', class_='tm-article-presenter')
    header = words.find('h1').text
    text = [i.text for i in soup.find_all('p')]
    dat_parse = {'header': header, 'text': text}
    return dat_parse

async def file_save(data: list):
    async with aiofiles.open('data.json', 'w', encoding='utf-8') as f:
        await f.write(str(data))

асинк def main(url: str):
    sites_dat = []
    sites_data = await scrap(url)
    data = await extract_urls(sites_data)

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [process_page(url) for url in data]
        results = await asyncio.gather(*tasks)

    sites_dat.extend(results)
    await file_save(sites_dat)

for name in main:
    print(name)
    