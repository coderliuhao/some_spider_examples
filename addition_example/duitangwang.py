# -*- coding: utf-8 -*- 
# @Time : 2021/1/29 13:13
# @Version: 3.8.5
# @Author : liu hao 
# @File : duitangwang.py.py

import requests
import asyncio
import aiohttp
from lxml import etree


async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    first_url = "https://www.duitang.com/search/?kw=%E7%BE%8E%E5%A5%B3&type=feed#!s"
    rest_urls = ["https://www.duitang.com/search/?kw=%E7%BE%8E%E5%A5%B3&type=feed#!s-p{}".format(page) for page in range(2,31)]
    rest_urls.append(first_url)
    futures = [get_response(url) for url in rest_urls]
    responses = await asyncio.gather(*futures)
    page = 1
    for response in responses:
        html = etree.HTML(response)
        images = html.xpath("//div[@class='mbpho']/a/img")
        image_src = [image.get("src") for image in images]
        idx = 1
        for src in image_src:
            img = requests.get(src)
            with open(f"{page}{idx}"+".jpg","wb") as f:
                f.write(img.content)
                f.close()
            idx+=1
        page+=1

    return 0

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())








