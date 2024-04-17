import multiprocessing, time, random
# под вопросом как работает....

def worker(num, arr):
    pid_proc = multiprocessing.current_process().pid
    # блокируем доступ к массиву из других потоков
    arr.acquire()
    try:
        for _ in range(3):
            # имитируем нагрузку, для того, что бы была
            # конкуренция доступа к общему ресурсу (очереди)
            time.sleep(random.uniform(0.01, 0.1))
            # последовательно изменяем элемент
            # массива на PID процесса 3 раза
            arr[num.value] = pid_proc
            # счетчик элементов массива
            num.value = num.value + 1
    finally:
        # завершаем процесс и разрешаем
        # доступ к массиву другим процессам
        arr.release()


if __name__ == '__main__':
    # создаем общий объект для процессов
    num = multiprocessing.Value('i', 0)
    # создаем общий массив для процессов   range(1000)
    arr = multiprocessing.Array('i', 10)

    procs = []
    for _ in range(3):
        proc = multiprocessing.Process(target=worker, args=(num, arr))
        procs.append(proc)
        proc.start()

    # Ждем результатов
    [proc.join() for proc in procs]
    print('Вывод результатов:')
    print([i for i in arr if i != 0])
    # очищаем используемые ресурсы
    [proc.close() for proc in procs]

# Вывод результатов:
# [28690, 28690, 28690, 28691, 28691, 28691, 28692, 28692, 28692]