import multiprocessing
# Весь код работает многопроцессорно, но из-за того, что несколько
# процессов работают с одной переменной, может возникнуть проблема гонки
# данных (race condition), когда результат выполнения программы может быть
# непредсказуемым.
# В нашем случае каждый из процессов работает со своей переменной counter. 5
# процессов — 5 переменных со значением 10000 в финале03_process-1.py
counter = 0


def increment():
    global counter
    for _ in range(10_000):
        counter += 1
        print(f"Значение счетчика: {counter:_}")


if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=increment)
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(f"Значение счетчика: {counter:_}")
