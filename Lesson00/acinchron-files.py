import asyncio
from pathlib import Path

async def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
        # do some processing with the file contents
        print(f'{f.name} содержит {contents[:7]}...')
async def main():
    dir_path = Path('/path/to/directory')
    dir_path = Path('.')
    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]
    tasks = [asyncio.create_task(process_file(file_path)) for file_path in file_paths]
    await asyncio.gather(*tasks)
if __name__ == '__main__':
    asyncio.run(main())
# Программа для асинхронной обработки большого количества файлов из примера 2
# работает следующим образом:
# 1. Определяется путь к директории, в которой находятся файлы, которые нужно
# обработать.
# 2. Используется метод iterdir() для получения списка файлов в каталоге, и метод
# is_file() для проверки, что это файлы, а не каталоги или другие объекты.
# 3. Создается список задач для обработки каждого файла с помощью функции
# asyncio.create_task(), где каждая задача вызывает функцию process_file() для
# обработки соответствующего файла.
# 4. Запускается выполнение всех задач с помощью функции asyncio.gather().
# 5. Когда все задачи завершены, программа завершается.
# Функция process_file() открывает файл для чтения и считывает его содержимое с
# помощью метода read(). Затем происходит обработка содержимого файла (которая
# может быть любой, в зависимости от требований конкретной задачи). После этого
# файл закрывается.

