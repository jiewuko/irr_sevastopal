import base64

import scrapy
from ..items import IrrSevastopalItem
import json
from datetime import datetime, timedelta

from scrapy.utils.project import get_project_settings

project_settings = get_project_settings()
URL = project_settings.get('URL')


class IrrSpider(scrapy.Spider):
    name = 'IrrSpider'
    allowed_domains = ['irr.ru']

    def start_requests(self):
        yield scrapy.Request(
            url='https://irr.ru/real-estate/{}'.format(URL),
            callback=self.parse
        )

    def parse(self, response):
        urls = response.xpath('//div[contains(@class, "listing__itemTitleWrapper")]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_announcement)

        pagination_urls = response.xpath("//li[contains(@class, 'pagination__pagesItem')]//a/@href").extract()
        for pagination_url in pagination_urls:
            if pagination_url:
                yield scrapy.Request(url='https://irr.ru' + pagination_url,
                                     callback=self.parse)

    def parse_announcement(self, response):
        items = IrrSevastopalItem()
        data = json.loads(list(filter(lambda i: 'retailrocket.products.post' in i, response.xpath(
            "//script/text()").extract()))[0].split('retailrocket.products.post(')[1].split('\n')[0][:-2])
        now = datetime.now()
        if (now - datetime.strptime(data.get(
                'params').get('date_create'), '%Y-%m-%d %H:%M:%S')) > timedelta(hours=120):
            print('Время публикации объявления {} более 120 часов назад'.format(response.url))
            return
        items['url'] = response.url
        items['name'] = response.xpath("//h1/text()").extract_first().strip()
        items['description'] = ' '.join(''.join(response.xpath(
            "//p[contains(@itemprop, 'description')]//text()").extract()).strip().replace('\n', '').split())
        items['subcategory'] = ' '.join(''.join(response.xpath(
            "//li[contains(@itemprop, 'itemListElement')]//a//text()").extract()).split())
        items['address'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__infoTextBold js-scrollToMap')]//text()").extract()).strip()
        items['published_date'] = datetime.strptime(data.get('params').get('date_create'), '%Y-%m-%d %H:%M:%S')
        items['price'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__price js-contentPrice')]//text()").extract()).strip().replace(
            '\xa0', '.')
        items['telephone'] = base64.b64decode(
            response.xpath("//input[contains(@name, 'phoneBase64')]//@value").extract_first()).decode('utf-8')
        items['agency'] = 'IRR'
        yield items
