import scrapy
from scrapy import Request
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)

base_url = "http://www.lrts.me"


# start_urls = 'http://www.lrts.me/explore/anchor/verify'


class LanrenAnchorsDetailSpider(scrapy.Spider):
    name = 'lanren_anchors_detail'

    start_urls = [base_url]

    def parse(self, response):
        list_category = response.xpath('/html/body/div[1]/div[1]/div[1]/ul/li')
        # print('list_anchors={}'.format(list_anchors))

        # 遍历改页所有的专辑类别---仅搜有声书
        for category in list_category[:13]:
            category_name = category.xpath('./a/span/text()').extract_first()
            # logger.info(category_name)

            category_href = category.xpath('./a/@href').extract_first()
            if category_href:
                category_href = base_url + category_href

                for tail in ['/recommend', '/latest', '/hot']:
                    # 根据 category_href 去下一层获取所有的节目
                    logger.info('category_name={}, tail={}'.format(category_name,category_href + tail))
                    yield Request(category_href + tail, callback=self.list_parse)
                    # break

    def list_parse(self, response):
        # 重要 #
        list_book = response.xpath('/html/body/div[1]/div[2]/div[1]/section[2]/div[3]/ul/li')

        for book in list_book:
            book_name = book.xpath('./div[2]/a/text()').extract_first()
            book_href = book.xpath('./div[2]/div[1]/a[2]/@href').extract_first()

            # 根据 book_href 去下一层获取所有的节目
            yield Request(base_url + book_href, callback=self.host_parse)

            # break
        ## 分页
        next_page_href = response.xpath('//*[@class="next"]/@href').extract_first()
        if next_page_href:
            next_page_href = base_url + next_page_href
            ## 根据 next_page_href 去所有的节目
            yield Request(next_page_href, callback=self.list_parse)

    def host_parse(self, response):

        item = {}
        item['anchor_name'] = response.xpath('//*[@class="userinfo"]/h2/text()').extract_first()
        item['anchor_addr'] = response.xpath('/html/body/section/aside/div[2]/ul/li[1]/div/text()').extract_first()
        item['program_nums'] = response.xpath('/html/body/section/aside/ol/li[1]/a/span/text()').extract_first()
        item['follower_nums'] = response.xpath('/html/body/section/aside/ol/li[3]/a/span/text()').extract_first()
        item['attention_nums'] = response.xpath('/html/body/section/aside/ol/li[2]/a/span/text()').extract_first()
        item['anchor_avatar'] = response.xpath('/html/body/section/aside/div[1]/a/img/@src').extract_first()
        # print(item)
        yield item
