# Создать программу, которая будет производить подсчет количества слов в каждом файле в
# указанной директории и выводить результаты в консоль.
# Используйте потоки.

import os
import threading
import logging
import time

from pathlib import Path

logger = logging.getLogger(__name__)


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        counts_word = len(contents.split())
        print(f'{f.name} содержит {counts_word} слов')
        # logger.info(f'{f.name} содержит {counts_word} слов')


def main():
    dir_path = Path('.')
    file_paths = os.walk(dir_path)

    threads = []
    for root, dirs, files in file_paths:
        for file in files:
            t = threading.Thread(target=process_file(os.path.join(root, file)))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

print('Finish')


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'{time.time() - start_time: .2f}')