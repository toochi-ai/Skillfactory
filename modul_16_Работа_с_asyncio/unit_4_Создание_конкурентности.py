import asyncio
import time


async def set_after(fut, delay, value):
    # асинхронное ожидание в течение заданного времени
    await asyncio.sleep(delay)

    # устанавливаем значение футуры fut
    fut.set_result(value)


async def main():
    # Получаем объект цикла событий
    loop = asyncio.get_running_loop()

    # Создаем объект футуры при помощи метода create_future()
    fut = loop.create_future()

    # делаем из корутины set_after асинхронную задачу
    # передаем ей в качестве аргумента футуру, задержку и остальные параметры
    # помним что create_task ставит задачу в расписание на выполнение
    await loop.create_task(
        set_after(fut, 1, '... world'))

    print('hello ...')

    # ждем пока футура перейдет в конечное состояние
    print(await fut)


# запуск основной корутины main()
asyncio.run(main())

print('---')


async def async_func(taskMark, delay, retValue):
    print(f'Асинхронная задача {taskMark} начата')
    await asyncio.sleep(delay)
    print(f'Асинхронная задача {taskMark} завершена')
    return retValue


async def main():
    result = await asyncio.gather(async_func(1, 1, 1),
                                  async_func(2, 2, 2),
                                  async_func(3, 3, 3))
    print(result)


if __name__ == "__main__":
    tm = time.time()
    asyncio.run(main())
    print(f'Общее время выполнения {time.time() - tm}')
print('---')


# определяем корутину
# mark - метка с которой вызывается корутина
# delay - задержка перед завершением
# retValue - результат который вернет корутина
async def async_func(taskMark, delay, retValue):
    print(f'Асинхронная задача {taskMark} начата')
    await asyncio.sleep(delay)
    print(f'Асинхронная задача {taskMark} завершена')
    return retValue


async def main():
    # запускаем 3 задачи для конкурентного выполнения
    await asyncio.wait((async_func(1, 1, 1),
                        async_func(2, 2, 2),
                        async_func(3, 3, 3)))

    if __name__ == "__main__":
        tm = time.time()
        asyncio.run(main())
        print(f'Общее время выполнения {time.time() - tm}')
