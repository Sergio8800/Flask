import os
import asyncio
import time
from pathlib import Path


async def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        counts_word = len(contents.split())
    print(f'{f.name} содержит {counts_word} слов')

async def main():
    tasks = []
    dir_path = Path('.')
    file_paths = os.walk(dir_path)
    for root, dirs, files in file_paths:
        for file in files:
            task = asyncio.create_task(process_file(os.path.join(root, file)))
            tasks.append(task)
    await asyncio.gather(*tasks)



if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print('Finish')
    print(f'{time.time() - start_time: .2f}')