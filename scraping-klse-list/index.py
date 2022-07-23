import time
import requests
import random
import json
import pandas as pd
from queue import Queue
from threading import Thread, Lock
from time import perf_counter

random.seed(time.time())

listed_companies_url: str = 'https://www.bursamalaysia.com/api/v1/listed_companies/companies'

klse_categories: list = ['MAIN-MKT', 'ACE-MKT', 'LEAP-MKT']

userAgents: list = ['Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
                    'Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
                    'Mozilla/5.0 (Linux; Android 11; CPH1937) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36']

headers = {'user-agent': random.choice(userAgents),
           'accept-encoding': 'gzip, deflate',
           'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'x-csrf-token': 'ifBy9AGuGfyywKn6e2+uyH19FYDw9mgjaJeHvoFX1eTtvY0v+ZyHfHS7JROFB/CWiTFAA0R0glCU47ht5ejs/Q=='
           }


cookies = {'_locomotiveapp_session': 'MTQxVFd1aXZnekhZNFlsbTcrYm9haENJa0FCbXpuNTN5WW1wcmFaMTdHREZsa281T3lIVHQ0NEkrSzhqRGhHbWoySmxEbVJucFNxc05kMz'
                                     'BGQ0pGcGJ5SSs5bldaY2Y5OG1KNTlIdVY4MDVDZmZSRHArYm1UUTNEcWFnN1FQbmthZ0piYmh4Nys1YWx4YXg0M3BTK3ZRPT0tLXl6djQ0d'
                                     'GhtbnMzYW1zZll5akdodGc9PQ==--caad8b3d1f2f987432ca17da0172e955366ff4b4'}

payload = {'draw': '1',
           'columns': [
               {'data': 'index', 'name': '', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
               {'data': 'stock_id', 'name': '', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
               {'data': 'name', 'name': '', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
               {'data': 'website', 'name': '', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}}
           ],
           'order': [{'column': 0, 'dir': 'asc'}],
           'start': 0,
           'length': -1,
           'search': {'value': '', 'regex': 'false'},
           'category': 'MAIN-MKT',
           'company_id': 'Select Company'
           }

compannies_list: pd.DataFrame = pd.DataFrame()


class Klse(object):

    def __init__(self,
                 name: str,
                 url: str,
                 data: dict,
                 cookies: dict,
                 headers: dict):
        self.url = url
        self.name = name
        self.data = data
        self.cookies = cookies
        self.headers = headers
        self.companies = None
        self.success = False
        self.error = None

    def download(self) -> bool:
        try:
            pass
            response = requests.post(self.url, data=self.data, cookies=self.cookies, headers=self.headers)
            json_data = json.loads(response.text)
            tmp_companies = pd.DataFrame.from_dict(json_data['data'])
            tmp_companies.drop(columns=['index'], axis=1, inplace=True)
            tmp_companies.loc[:, ['category']] = self.data['category']
            self.companies = tmp_companies
            self.success = True
        except Exception as e:
            self.error = e

        return self.success

    def all_companies(self):
        return self.companies


class Downloader(Thread):

    def __init__(self, q, lock: Lock):
        Thread.__init__(self)
        self.queue = q
        self.lock = lock

    def run(self):
        global compannies_list

        while not self.queue.empty():
            item: Klse = self.queue.get()
            if item.download():
                compannies_list = pd.concat([compannies_list, item.all_companies()], ignore_index=True)

            self.queue.task_done()


if __name__ == '__main__':

    queue = Queue(0)

    threads: list = []
    companies: pd.DataFrame = pd.DataFrame()
    start_time = perf_counter()
    lock = Lock()

    for category in klse_categories:
        payload['category'] = category
        user_agent = userAgents[random.randint(0, len(userAgents)-1)]
        headers['user-agent'] = user_agent
        obj = Klse(name=category, url=listed_companies_url, data=payload.copy(), cookies=cookies, headers=headers.copy())
        queue.put(obj)

    for _ in range(3):
        thread = Downloader(q=queue, lock=lock)
        thread.start()
        threads.append(thread)

    queue.join()

    for i in threads:
        i.join()

    print(compannies_list)

    end_time = perf_counter()
    print(f'Exacuted time: {end_time - start_time} seconds.')


