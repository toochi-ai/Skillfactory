import random
import threading

gX = 0
threadsInfo = {}
lock = threading.Lock()


def threadFunc(threadMark):
    print('thread started')
    global gX
    while True:
        with lock:
            if gX >= 10000:
                break

            gX = gX + 1
            threadsInfo[threadMark] += 1
            print(f'thread {threadMark}: {gX}')


if __name__ == "__main__":
    threads = []
    for i in range(3):
        threadMark = f'Thread - {i}'
        threadsInfo[threadMark] = 0
        thread = threading.Thread(target=threadFunc, args=(threadMark,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(threadsInfo)
print('---')


# Попытка сделать потокобезопасный класс
class SomeLockClass:
    def __init__(self):
        # внутренние переменные
        self.a = 1
        self.b = 2
        # внутренний лок
        self.lock = threading.RLock()

    # потокобезопасный метод изменения параметра а
    def changeA(self, a):
        with self.lock:
            self.a = a

    # потокобезопасный метод изменения параметра b
    def changeB(self, b):
        with self.lock:
            self.b = b

    # потокобезопасный метод одновременной смены параметров
    def changeAB(self, a, b):
        # зачем-то мы ещё раз используем лок перед вызовом и без того потокобезопасных методов
        with self.lock:
            self.changeA(a)  # зависания не будет
            self.changeB(b)


# максимальный размер произведённой продукции
g_maxProduct = 100
# переменная склада
g_storage = []
# лок
g_lock = threading.Lock()


def producer():
    # код производителя
    for i in range(g_maxProduct):
        with g_lock:
            # отправляем продукцию на склад
            g_storage.append(random.randint(0, 100))


def consumer():
    # код потребителя
    pop_count = 0
    while True:
        with g_lock:
            # получаем продукцию со склада
            if g_storage:
                pop_count += 1
                print(f"{pop_count}: {g_storage.pop()}")
        if pop_count == g_maxProduct:
            break


if __name__ == '__main__':
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
print('---')

g_maxProduct = 100
g_storage = []
g_lock = threading.BoundedSemaphore(3)


def producer():
    for i in range(g_maxProduct):
        g_lock.acquire()
        g_storage.append(random.randint(0, 100))


def consumer():
    pop_count = 0
    while True:
        if g_storage:
            pop_count += 1
            print(f"{pop_count}: {g_storage.pop()}")
            g_lock.release()
        if pop_count == g_maxProduct:
            break


if __name__ == '__main__':
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
