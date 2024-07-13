import asyncio


# async def first():
#     print("first started")
#     await asyncio.sleep(5)
#     print("first finished")
#     return "first result"


# async def second():
#     print("second started")
#     await asyncio.sleep(5)
#     print("second finished")
#     return "second result"


# async def third():
#     print("third started")
#     await asyncio.sleep(5)
#     print("third finished")
#     return "third result"


# async def myfunc():
#     a = await first()
#     b = await second()
#     c = await third()
#     print(a, b, c)


# asyncio.run(myfunc())


async def count_to_three():
    print("Веду отсчёт. 1")
    await asyncio.sleep(1)
    print("Веду отсчёт. 2")
    await asyncio.sleep(2)
    print("Веду отсчёт. 3")
    await asyncio.sleep(3)


coroutine_counter = count_to_three()
print(coroutine_counter)
coroutine_counter.send(None)
coroutine_counter.send(None)
coroutine_counter.send(None)