import requests
import os
import concurrent.futures
import aiohttp
import asyncio
from urllib.parse import urlparse
import argparse
import time


# Функция для загрузки изображений с использованием многопоточности
def download_images_multithread(image_urls, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    start_time = time.time()

    def download_image(url):
        try:
            response = requests.get(url)
            image_name = os.path.basename(urlparse(url).path)
            with open(os.path.join(save_folder, image_name), 'wb') as f:
                f.write(response.content)
            end_time = time.time()
            print(f"Изображение {image_name} успешно сохранено. Время скачивания: {end_time - start_time:.2f} сек.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения по адресу {url}: {e}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, image_urls)

    total_time = time.time() - start_time
    print(f"Общее время выполнения программы: {total_time:.2f} сек.")


# Функция для загрузки изображений с использованием многопроцессорности
def download_images_multiprocess(image_urls, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    start_time = time.time()

    def download_image(url):
        try:
            response = requests.get(url)
            image_name = os.path.basename(urlparse(url).path)
            with open(os.path.join(save_folder, image_name), 'wb') as f:
                f.write(response.content)
            end_time = time.time()
            print(f"Изображение {image_name} успешно сохранено. Время скачивания: {end_time - start_time:.2f} сек.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения по адресу {url}: {e}")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(download_image, image_urls)

    total_time = time.time() - start_time
    print(f"Общее время выполнения программы: {total_time:.2f} сек.")


# Функция для загрузки изображений с использованием асинхронного подхода
async def download_images_async(image_urls, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        async def download_image(url):
            try:
                async with session.get(url) as response:
                    image_name = os.path.basename(urlparse(url).path)
                    with open(os.path.join(save_folder, image_name), 'wb') as f:
                        f.write(await response.read())
                    end_time = time.time()
                    print(
                        f"Изображение {image_name} успешно сохранено. Время скачивания: "
                        f"{end_time - start_time:.2f} сек.")
            except Exception as e:
                print(f"Ошибка при загрузке изображения по адресу {url}: {e}")

        await asyncio.gather(*[download_image(url) for url in image_urls])

    total_time = time.time() - start_time
    print(f"Общее время выполнения программы: {total_time:.2f} сек.")


def main():
    parser = argparse.ArgumentParser(description='Download images from given URLs.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+', help='URLs of images to download')
    parser.add_argument('-o', '--output', type=str, help='Output folder to save images',
                        default='downloaded_images')
    args = parser.parse_args()

    image_urls = args.urls
    save_folder = args.output

    print("Скачивание изображений с использованием многопоточности:")
    download_images_multithread(image_urls, save_folder)

    print("\nСкачивание изображений с использованием многопроцессорности:")
    download_images_multiprocess(image_urls, save_folder)

    print("\nСкачивание изображений с использованием асинхронного подхода:")
    asyncio.run(download_images_async(image_urls, save_folder))


if __name__ == "__main__":
    main()
