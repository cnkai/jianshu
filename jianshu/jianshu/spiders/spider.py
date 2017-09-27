from scrapy import Spider, Request
from jianshu.items import JianshuItem
from lxml import etree
import re

class JianshuSpider(Spider):

    name = 'jianshu'
    init_following_url = 'http://www.jianshu.com/users/3aa040bf0610/following'

    '''
    主要逻辑：
    从某一个链接开始，作为起始点，直接获取它的个人信息，进行存储
    另外，还要根据它的关注者数，计算出页面数，对每一页的个人信息进行抓取
    获取它的个人全部关注者列表，并且对其中的每一个人进行同样的操作。
    '''
    def start_requests(self):
        yield Request(url = self.init_following_url, callback = self.parse_following)

    def parse_following(self, response):
        '''
        主要用来解析用户信息和页码
        :param response:
        :return:
        '''
        selector = etree.HTML(response.text)
        # 下面是解析用户信息，用户信息全部在第一页进行解析
        item = JianshuItem()
        id = selector.xpath('//div[@class="main-top"]/div[@class="title"]/a/@href')[0]
        item['id'] = re.search('/u/(.*)', id).group(1)
        item['name'] = selector.xpath('//div[@class="main-top"]/div[@class="title"]/a/text()')[0]
        item['followings'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[1]//p/text()')[0]
        item['followers'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[2]//p/text()')[0]
        item['articles'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[3]//p/text()')[0]
        item['words'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[4]//p/text()')[0]
        item['likes'] = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[5]//p/text()')[0]
        yield item

        # 下面是获取关注者页码数，每一页进行请求
        page_all = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul/li[1]//p/text()')[0]
        page_all = int(page_all)
        if page_all % 9 == 0:
            page_num = int(page_all / 9)
        else:
            page_num = int(page_all / 9) + 1
        for i in range(1, page_num):
            url = response.url + '?page={}'.format(str(i+1))
            yield Request(url=url, callback=self.parse_info)

    def parse_info(self, response):
        '''
        对页面信息进行解析，同时跟进链接
        :param response:
        :return:
        '''
        # 获取它的关注者列表，再次发起请求
        selector = etree.HTML(response.text)
        id_list = selector.xpath('//div[@class="info"]/a/@href')
        for id in id_list:
            id = re.search('/u/(.*)', id).group(1)
            url = 'http://www.jianshu.com/users/{}/following'.format(id)
            yield Request(url=url, callback=self.parse_following)






