from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class MyUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent = crawler.settings.get('USER_AGENT')
        )

    def process_request(self, request, spider):
        random_useragent = random.choice(self.user_agent)
        request.headers.setdefault("User-Agent", random_useragent)
