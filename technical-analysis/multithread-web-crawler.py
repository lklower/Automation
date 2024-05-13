import os
import threading
import time
from queue import Queue
from threading import Lock

import requests
from requests.exceptions import SSLError, ConnectionError

from classes import link_scraper as ls
from classes import webcrawler

import secrets
import string

linkSearcher = ls.LinkSearcher(
    target_url='https://www.getright.com.my/skjdgdgdg',
    fields=None,
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77'})
success: bool = linkSearcher.run()

links: list = linkSearcher.get_links()
for link in links:
    print(link, end='\n')
print(f'Total {len(links )} links found!')

# url = 'https://ws20.bursamalaysia.com/api/v2/stock_price_data?stock_code=7214.MY&mode=historical&from_date=20170721&ws_a=311e870c5af39fcd6a7a5e565a05a47b6074f23052ad0b03311109e364c7e8d7&ws_m=1658731130.0'
#
# data = {
#     'stock_code': '7214.MY',
#     'mode': 'historical',
#     'from_date': '20170721',
#     'ws_a': '311e870c5af39fcd6a7a5e565a05a47b6074f23052ad0b03311109e364c7e8d7',
#     'ws_m': '1658731130.0'
# }


class Target(object):

    def __init__(
            self,
            url: str,
            data=None,
            cookies=None,
            headers=None,
            save_path=None):
        self.url: str = url
        self.data = data
        self.cookies = cookies
        self.headers = headers
        self.success: bool = False
        self.connnect = None
        self.error = None
        self.content = 'lklower'
        self.destination = save_path

    def download(self) -> bool:
        response = None
        try:
            if self.connnect is None:
                self.connnect = requests.Session()

            response = self.connnect.get(self.url, data=self.data, cookies=self.cookies, headers=self.headers)
            if response.status_code == 200:
                self.content = response.content.decode()
                self.success = True
        except ConnectionError as error_msg:
            self.error = error_msg
        except Exception as error_msg:
            self.error = error_msg
        finally:
            if response is not None:
                response.close()

            self.close()

        return self.success

    def close(self):
        if self.connnect is not None:
            self.connnect.close()
            self.connnect = None

    def data(self):
        return self.content

    def save_to(self, path=None):
        if path is not None:
            self.destination = path

        if self.destination is None:
            return False

        if os.path.exists(path=self.destination) is False:
            return False

        try:
            with open(file=os.path.join(self.destination, f'lklow.txt'), mode='w') as w:
                w.write(self.content)
        except IOError as e:
            self.error = e
            return False
        finally:
            w.close()
            print('exit!')

        return True


# target = Target(url='https://www.lklowstudio.com/', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})

# target.save_to(path='C://Users/User/Desktop/')


if __name__ == '__main__':
    report: dict[str, list] = {'success': [], 'failure': []}
    threads: list[threading.Thread] = []
    urls: Queue = Queue(maxsize=0)
    lock = Lock()
    urls.put('https://www.google.com/')
    urls.put('https://www.microsoft.com/')
    urls.put('https://colab.research.google.com/')
    urls.put('https://www.apple.com/')
    urls.put('https://www.sunway.com.my/')
    urls.put('https://www.microsoft.com/')
    urls.put('https://www.amazon.com/')
    urls.put('https://www.facebook.com/')

    start_time: float = time.perf_counter()
    try:

        for i in range(0, 3):
            t = webcrawler.Crawler(data=urls, lock=lock, report=report)
            t.daemon = True
            t.start()
            threads.append(t)

        urls.join()
        print('Done worked!')

        for thread in threads:
            thread.join()
            print(f'{thread.name} Done!')

    except SSLError as e:
        pass
    except ConnectionError as e:
        pass

    end_time: float = time.perf_counter()
    print(f'Total excuted time {end_time - start_time} seconds.')
