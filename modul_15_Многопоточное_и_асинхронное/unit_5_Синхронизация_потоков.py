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
