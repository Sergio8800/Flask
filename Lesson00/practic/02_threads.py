import os
import multiprocessing
import time

from pathlib import Path


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        counts_word = len(contents.split())
    print(f'{f.name} содержит {counts_word} слов')


if __name__ == '__main__':
    start_time = time.time()
    dir_path = Path('.')
    file_paths = os.walk(dir_path)
    processes = []
    for root, dirs, files in file_paths:
        for file in files:
            p = multiprocessing.Process(target=process_file, args=(os.path.join(root, file), ))
            processes.append(p)
            p.start()

    for p in processes:
        p.join()
    
    print('Finish')
    print(f'{time.time() - start_time: .2f}')