import asyncio


class GatewayError(Exception):
    pass


async def total_prices(codes,fetcher,limit=2,timeout=0.2):
    if type(limit) is not int or limit<1 or timeout<=0: raise ValueError('invalid resource limits')
    semaphore=asyncio.Semaphore(limit)
    async def one(code):
        async with semaphore:
            price=await fetcher(code)
            if type(price) is not int or price<0: raise GatewayError('invalid upstream price')
            return price
    async with asyncio.timeout(timeout):
        tasks=[asyncio.create_task(one(code)) for code in codes]
        try:
            return sum(await asyncio.gather(*tasks))
        finally:
            for task in tasks:
                if not task.done(): task.cancel()
            await asyncio.gather(*tasks,return_exceptions=True)
