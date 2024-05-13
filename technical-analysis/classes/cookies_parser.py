import re
from re import Pattern
from re import Match


class Cookie(object):
    def __init__(self, string: str):
        """
        :param string: raw data of cookies to parse.
        """
        self.raw_cookies = string

    def parse(self) -> str:
        patterns: list[Pattern] = [
            re.compile(r'expires=[^;]+;\s?', flags=re.I),
            re.compile(r'(?:path|domain|secure|httponly|max-age|samesite)(?:=[^;,]+)?;?,?', flags=re.I),
            re.compile(r'[\r\n\t ]'),
        ]

        _cookies: str = self.raw_cookies
        for pattern in patterns:
            _cookies = re.sub(pattern=pattern, repl='', string=_cookies)
        return _cookies

    def as_list(self) -> list[str]:
        l: list = []
        cookies = self.parse()

        if len(cookies) > 0:
            mateches: list[str] = re.findall(pattern=re.compile(r'([^;]+);'), string=cookies)
            for match in mateches:
                l.append(match)

        return l

    def as_dict(self) -> dict[str, str]:
        d: dict = {}

        cookies: list = self.as_list()
        for cookie in cookies:
            pattern: Pattern = re.compile(r'([^=]+)=(.*)$')
            match: Match = re.search(pattern=pattern, string=cookie)
            key, value = match.groups()
            d[key] = value

        return d
