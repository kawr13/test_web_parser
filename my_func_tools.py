import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs



async def srappers(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()


async def soup_text(sites: str):
    data = []
    soup = bs(sites, 'lxml')
    url_detailed = soup.find_all('a', class_='tm-title__link')
    for url in url_detailed:
        new = f"https://habr.com{url.get('href')}"
        data.append(new)
    return data



async def main(url: str):
    sites_dat = []
    sites_data = await srappers(url)
    data = await soup_text(sites_data)
    coros = [srappers(i) for i in data]
    for task in asyncio.as_completed(coros):
        words = await task
        soup = bs(words, 'lxml')
        words = soup.find('div', class_='tm-article-presenter')
        header = words.find('h1').text
        text = soup.find_all('p')
        lst = []
        for i in text:
            lst.append(i.text)
        dat_parse = {'header': header, 'text': lst}
        sites_dat.append(dat_parse)
    return sites_dat
        
        

  
    


if __name__ == "__main__":
    answ = 'pyhon'
    URL = rf'https://habr.com/ru/search/?q={answ}&target_type=posts&order=relevance'
    asyncio.run(main(URL))
    
