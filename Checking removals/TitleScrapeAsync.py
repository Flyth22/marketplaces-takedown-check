from title_scrape_functions import excel_to_pandas
from title_scrape_functions import excel_from_dataframe
import asyncio
import tqdm.asyncio
import tqdm
import aiohttp
import pandas as pd
import time
from bs4 import BeautifulSoup
import os

pd.options.mode.chained_assignment = None  # default='warn'

pd_listings_report = excel_to_pandas()

my_timeout = aiohttp.ClientTimeout(
    total=None,  # default value is 5 minutes, set to `None` for unlimited timeout
    sock_connect=60,  # How long to wait before an open socket allowed to connect
    sock_read=30  # How long to wait with no data being read before timing out
)


async def scrape(url):
    connector = aiohttp.TCPConnector(limit_per_host=10, limit=10)
    client = aiohttp.ClientSession(timeout=my_timeout, connector=connector, trust_env=True)
    async with client as session:
        try:
            async with session.get(url) as resp:
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')
                title = soup.select_one('title').text
                scraped_url = resp.url
                # count_active_tasks = len(asyncio.all_tasks())
                # print(count_active_tasks)
                return title, scraped_url

        # Exception noted for future inspection
        except (aiohttp.client_exceptions.ClientOSError, AttributeError, RuntimeError,
                aiohttp.client_exceptions.ServerTimeoutError, aiohttp.client_exceptions.ServerDisconnectedError,
                aiohttp.client_exceptions.ClientPayloadError, UnicodeDecodeError) as err:
            return err, err
        except Exception as err:
            return err, err


async def main():
    start_time = time.time()
    tasks = []
    for url in pd_listings_report["URL"]:
        task = asyncio.ensure_future(scrape(url))
        tasks.append(task)
    print(len(tasks))
    print('Saving the output of extracted information')
    responses = []
    for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        responses.append(await f)
    pd_listings_report["result"] = await asyncio.gather(*tasks)
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)


loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())

pd_listings_report['PAGE_TITLE'] = pd_listings_report['result'].apply(lambda x: list(x)[0])
pd_listings_report['SCRAPED_URL'] = pd_listings_report['result'].apply(lambda x: list(x)[1])
pd_listings_report = pd_listings_report.drop(['result'], axis=1)
excel_from_dataframe(pd_listings_report, "scraped_titles_")


input("Program finished! Thank you")
