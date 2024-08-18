import threading

gX = 0


def threadFunc(lock):
    print('thread started')
    global gX
    for i in range(100000):
        # захватываем лок, делая все операции далее монопольными
        lock.acquire()
        gX = gX + 1
        # освобождаем лок
        lock.release()


if __name__ == "__main__":
    gX = 0

    threads = []
    # создаём лок
    lock = threading.Lock()
    for i in range(5):
        # и передаём его в качестве аргумента в каждый поток
        threads.append(threading.Thread(target=threadFunc, args=(lock)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(gX)
