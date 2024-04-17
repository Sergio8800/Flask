import asyncio
from random import randint

import aiohttp  # асинхроный request
import time
import os
import datetime
from io import BytesIO
import requests
from PIL import Image

urls = ['https://www.britannica.com/animal/cat',
        'https://www.cats.org.uk/cats-blog/9-things-to-know-before-getting-your-first-cat',
        'https://www.smithsonianmag.com/smart-news/cats-prey-on-more-than-2000-different-species-180983429/',
        'https://www.python.org/',
        'https://pixabay.com/ru/',
        'https://gb.ru/',
        ]
IMG = ['jpeg', 'jpg']


# path = f'src/download/video_{datetime.datetime.now().time()}'
# my_path = os.getcwd() + "/" + "test_folder"  # путь к папке


def mkdir_new(pth):
    # my_path = os.getcwd() + "/" + "test_folder"
    my_path = os.path.join(os.getcwd(), "test_folder")
    my_path = os.path.join(my_path, pth.split('.')[-2])
    if not os.path.isdir(my_path):
        try:
            os.makedirs(my_path)
        except OSError:
            tmp = os.path.join(os.getcwd(), "test_mistake" + str(randint(10, 500)))
            os.makedirs(tmp)

    # try:
    #     # os.mkdir(my_path)
    #     if not os.path.isdir(my_path):
    #         os.makedirs(my_path)
    #         os.chdir(my_path)
    # except FileExistsError:
    #     os.chdir(my_path)
    return my_path


def main0(urls: []):
    for url in urls:
        # что бы получить начала строки, для добавление в случаии статического адресса(не обязательно использовать)
        html = url.replace('//', '=').split('/')[0].replace("=", "//")
        # html = url.split('/')[0]
        print(html)
        s = requests.get(url).text

        # через запись файла на диск ищем в нем строки с изображением.
        with open('file_tmp.txt', 'w', encoding="utf-8") as f:
            f.write(s)
            # f.writelines(s)
            img = []

            with open('file_tmp.txt', 'r', encoding='utf-8') as ff:
                for s in ff:
                    # coutt2 += 1
                    if '<img' in s:
                        s = s.split('<')[1].split('>')[0]
                        if "src=" in s:
                            s = s.split('src="')[1].split('"')[0]
                            img.append(s)
            # print(img)
            my_path = mkdir_new(html)
            get_img(img, my_path, html)
            # my_path = os.path.dirname(my_path.rstrip('/'))
            # print(my_path)


def get_img(mas: [], my_path, html):
    for img in mas:
        img_name = img.split('/')[-1]
        # print(img.split("/")[0])
        if img.split(".")[-1] != "jpg":
            continue
        if "http" not in img.split("/")[0]:
            img = html + "/" + img
        if img:
            response = requests.get(img)
            image = Image.open(BytesIO(response.content))
            new_file_path = os.path.join(my_path, img_name)
            try:
                image.save(new_file_path)
            except ValueError:
                continue
            # if image.format not in IMG:
            #     image = image.convert('RGB')

async def download(url):
    async with aiohttp.ClientSession() as session:

        html = url.replace('//', '=').split('/')[0].replace("=", "//")
        # html = url.split('/')[0]
        print(html)
        # s = requests.get(url).text

        async with session.get(url) as response:

            # text = await response.text()
            # filename = 'asyncio_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            s = await response.text()
            with open('file_tmp.txt', 'w', encoding="utf-8") as f:
                f.write(s)
                # f.writelines(s)
                img = []

                with open('file_tmp.txt', 'r', encoding='utf-8') as ff:
                    for s in ff:
                        # coutt2 += 1
                        if '<img' in s:
                            s = s.split('<')[1].split('>')[0]
                            if "src=" in s:
                                s = s.split('src="')[1].split('"')[0]
                                img.append(s)
                # print(img)
                my_path = mkdir_new(html)
                get_img(img, my_path, html)

        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()
if __name__ == '__main__':
    main0(urls)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Здесь мы используем модуль asyncio для асинхронной загрузки страниц. Мы
# создаем функцию download, которая использует aiohttp для получения
# html-страницы и сохранения ее в файл. Затем мы создаем асинхронную функцию
# main, которая запускает функцию download для каждого сайта из списка urls и
# ожидает их завершения с помощью метода gather. Мы запускаем функцию main с
# помощью цикла событий asyncio.
