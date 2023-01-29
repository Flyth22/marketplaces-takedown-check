from title_scrape_functions import excel_to_pandas
from title_scrape_functions import excel_from_dataframe
import asyncio
import tqdm.asyncio
import aiohttp
import pandas as pd
import time
from bs4 import BeautifulSoup

pd.options.mode.chained_assignment = None  # default='warn'

pd_listings_report = excel_to_pandas()

my_timeout = aiohttp.ClientTimeout(
    total=None,  # default value is 5 minutes, set to `None` for unlimited timeout
    sock_connect=10,  # How long to wait before an open socket allowed to connect
    sock_read=10  # How long to wait with no data being read before timing out
)


async def scrape(url):
    connector = aiohttp.TCPConnector(limit_per_host=70)
    client = aiohttp.ClientSession(timeout=my_timeout, connector=connector)
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
        except (aiohttp.client_exceptions.ClientOSError, AttributeError, RuntimeError,
                aiohttp.client_exceptions.ServerTimeoutError, aiohttp.client_exceptions.ServerDisconnectedError,
                aiohttp.client_exceptions.ClientPayloadError, UnicodeDecodeError) as err:
            return err, err


async def main():
    start_time = time.time()
    tasks = []
    for url in pd_listings_report["URL"]:
        task = asyncio.create_task(scrape(url))
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

pd_listings_report['Page_title'] = pd_listings_report['result'].apply(lambda x: list(x)[0])
pd_listings_report['scraped_url'] = pd_listings_report['result'].apply(lambda x: list(x)[1])

excel_from_dataframe(pd_listings_report, "scraped_titles_")
