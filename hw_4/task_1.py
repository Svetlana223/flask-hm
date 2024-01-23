'''
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
'''

import os.path
import requests
import threading
import time
from multiprocessing import Process
import asyncio
import aiohttp

urls = ['https://img.freepik.com/free-photo/forest-landscape_71767-127.jpg',
        'https://i.pinimg.com/236x/2a/f5/3d/2af53d8f1be483dd0e05b7b18142c33c.jpg',
        'https://img.freepik.com/free-photo/a-picture-of-fireworks-with-a-road-in-the-background_1340-43363.jpg'
        ]

folder = "downloaded_images"


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {filename}")


def download_images_threaded(urls):
    threads = []
    for index, url in enumerate(urls):
        filename = os.path.join(folder, f'image_{index}.jpg')
        thread = threading.Thread(target=download_image, args=(url, filename))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def download_images_multiprocess(urls):
    processes = []
    for index, url in enumerate(urls):
        filename = os.path.join(folder, f'image_{index}.jpg')
        process = Process(target=download_image, args=(url, filename))
        processes.append(process)
    for process in processes:
        process.start()
    for process in processes:
        process.join()


async def download_image_async(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as file:
                file.write(await response.read())
            print(f"Downloaded {filename}")


async def download_images_async(urls):
    tasks = []
    for index, url in enumerate(urls):
        filename = os.path.join(folder, f'image_{index}.jpg')
        task = asyncio.ensure_future(download_image_async(url, filename))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    if not os.path.exists(folder):
        os.makedirs(folder)

    start_time = time.time()

    print("Synchronous download:")
    for index, url in enumerate(urls):
        download_image(url, os.path.join(folder, f'image_{index}.jpg'))
    print(f"Synchronous download time: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    print("Threaded download:")
    download_images_threaded(urls)
    print(f"Threaded download time: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    print("Multiprocess download:")
    download_images_multiprocess(urls)
    print(f"Multiprocess download time: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    print("Asynchronous download:")
    asyncio.run(download_images_async(urls))
    print(f"Asynchronous download time: {time.time() - start_time:.2f} seconds")