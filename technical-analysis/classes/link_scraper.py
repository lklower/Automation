from re import Match
from urllib3 import PoolManager
from urllib3.response import HTTPResponse
from urllib3.exceptions import MaxRetryError
from lxml import html
import cookies_parser
import re


def get_response_cookies(response: HTTPResponse) -> list:
    cookies: list = []

    if response.status == 200:
        headers = response.headers
        if 'set-cookie' in headers.keys():
            cookies = cookies_parser.Cookie(string=headers['set-cookie']).as_list()

    return cookies


def is_url_validate(url: str) -> bool:
    url_pattern = re.compile(r'^https?://([^/]+)((?:/[^?]+)+)?/?(\?.*)?$', flags=re.I)
    match: Match = re.match(pattern=url_pattern, string=url)
    return True if match else False


def searching(string: str) -> list[str]:
    l: list = []

    if len(string) <= 0:
        return l

    tree = html.fromstring(html=string)

    elements: list = tree.xpath('//html/body//a[@href != "#" and @href != "" and @href != "/"]/@href')
    for element in elements:
        l.append(element)

    return l


class LinkSearcher(object):
    """
    :param target_url: string of url address
    """

    def __init__(self, target_url: str, method: str = 'GET', fields=None, headers=None):
        self.url: str = target_url
        self.fields = fields
        self.headers = headers
        self.method: str = method
        self.body: str = ''
        self.error: str = ''

        pattern = re.compile(r'^https?:\\/\\/([^\\/]+)((?:\\/[^\\/]+)+)?$')
        match: Match = re.match(pattern=pattern, string=self.url)
        if match is not None:
            self.url = f'{self.url}/'

    def run(self) -> bool:
        done = False
        manager: PoolManager = PoolManager()
        response: HTTPResponse

        try:
            response = manager.request(method=self.method, url=self.url, fields=self.fields, headers=self.headers, redirect=True)

            if response.status != 200:
                self.error = response.status
                return done

            cookies = get_response_cookies(response)
            response.close()

            if len(cookies) > 0:
                self.headers['cookie'] = ';'.join(cookies)

            response = manager.request(method=self.method, url=self.url, fields=self.fields, headers=self.headers, redirect=True)
            self.body = response.data.decode('utf-8')
            response.close()

            done = True
        except MaxRetryError as e:
            self.error = e
        finally:
            manager.clear()

        return done

    def get_links(self) -> list[str]:
        tmp_list: list = []

        pattern = re.compile(r'^/\b.*$')
        link_list: list = searching(self.body)

        for index, link in enumerate(link_list):
            new_str = re.sub(pattern=pattern, repl=f'{self.url[:-1]}{link_list[index]}', string=link)
            tmp_list.append(new_str)

        cp_tmp_list = tmp_list.copy()
        for link in cp_tmp_list:
            if is_url_validate(link) is not True:
                tmp_list.remove(link)

        return tmp_list
