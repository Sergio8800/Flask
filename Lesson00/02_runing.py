import threading
counter = 0
# Многопоточный код позволяет выполнять несколько задач параллельно, что может
# значительно ускорить выполнение программы. Однако при работе с общими
# ресурсами (например, глобальными переменными) может возникнуть проблема
# гонки данных, которую необходимо учитывать при написании многопоточного кода.
def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1
    print(f"Значение счетчика: {counter:_}")
threads = []
for i in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print(f"Значение счетчика в финале: {counter:_}")