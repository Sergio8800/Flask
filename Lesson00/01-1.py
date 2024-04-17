import threading
import time
# в отличие от предыдущего примера, потоки запускаются и
# завершаются последовательно, блокируя выполнение программы на время
# выполнения каждого потока.
def worker(num):
    print(f"Начало работы потока {num}")
    time.sleep(3)
    print(f"Конец работы потока {num}")
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i, ))
    threads.append(t)
for t in threads:
    t.start()
    t.join()
print("Все потоки завершили работу")