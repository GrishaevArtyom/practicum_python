import asyncio

async def async_task(name):
    print(f"Асинхронная задача {name} началась")
    await asyncio.sleep(2)
    print(f"Асинхронная задача {name} завершена")

async def main():
    await asyncio.gather(*(async_task(f"Задача {i+1}") for i in range(5)))

asyncio.run(main())