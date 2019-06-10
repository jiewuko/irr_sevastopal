import base64
import os
import csv
import scrapy
from ..items import IrrSevastopalItem
import json
from datetime import datetime, timedelta

from scrapy.utils.project import get_project_settings

project_settings = get_project_settings()
data = project_settings.get('DATA')


class IrrSpider(scrapy.Spider):
    name = 'IrrSpider'
    allowed_domains = ['irr.ru']

    def start_requests(self):
        with open(os.getcwd() + '/config.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i in (list(csv_reader)[1:]):
                country = i[0] + '.' if i[0] else ''
                category = i[1]
                sub_category = i[2]
                type_ = i[3]
                hours = i[4]
                url = data.get('Категория').get(category).get('Тип').get(type_).get(sub_category)
                yield scrapy.Request(
                    url='https://{}irr.ru/real-estate/{}'.format(country, url),
                    callback=self.parse,
                    meta={
                        'category': category,
                        'sub_category': sub_category,
                        'type_': type_,
                        'hours': hours,
                    },
                    dont_filter=True,
                )

    def parse(self, response):
        urls = response.xpath('//div[contains(@class, "listing__itemTitleWrapper")]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_announcement,
                                 meta={
                                     'category': response.meta.get('category'),
                                     'sub_category': response.meta.get('sub_category'),
                                     'type_': response.meta.get('type_'),
                                     'hours': response.meta.get('hours'),
                                 },
                                 )

        pagination_urls = response.xpath("//li[contains(@class, 'pagination__pagesItem')]//a/@href").extract()
        for pagination_url in pagination_urls:
            if pagination_url:
                yield scrapy.Request(url='https://irr.ru' + pagination_url,
                                     callback=self.parse,
                                     meta={
                                         'category': response.meta.get('category'),
                                         'sub_category': response.meta.get('sub_category'),
                                         'type_': response.meta.get('type_'),
                                         'hours': response.meta.get('hours'),
                                     },
                                     )

    def parse_announcement(self, response):
        items = IrrSevastopalItem()

        category = response.meta.get('category')
        sub_category = response.meta.get('sub_category')
        type_ = response.meta.get('type_')
        hours = int(response.meta.get('hours'))
        owner_name = response.xpath(
            "//div[contains(@class, 'productPage__infoTextBold productPage__infoTextBold_inline')]/"
            "text()").extract_first()
        data_from_site = json.loads(list(filter(lambda i: 'retailrocket.products.post' in i, response.xpath(
            "//script/text()").extract()))[0].split('retailrocket.products.post(')[1].split('\n')[0][:-2])

        now = datetime.now()
        if (now - datetime.strptime(data_from_site.get('params').get(
                'date_create'), '%Y-%m-%d %H:%M:%S')) > timedelta(hours=hours):
            print('Время публикации объявления {} более {} часов назад'.format(response.url, hours))
            return

        items['url'] = response.url
        items['title'] = response.xpath("//h1/text()").extract_first().strip()
        items['description'] = ' '.join(''.join(response.xpath(
            "//p[contains(@itemprop, 'description')]//text()").extract()).strip().replace('\n', '').split())
        items['category'] = category
        items['subcategory'] = sub_category
        items['type_'] = type_
        items['owner_name'] = owner_name.strip() if owner_name else None
        items['address'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__infoTextBold js-scrollToMap')]//text()").extract()).strip()
        items['published_date'] = datetime.strptime(
            data_from_site.get('params').get('date_create'), '%Y-%m-%d %H:%M:%S')
        items['price'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__price js-contentPrice')]//text()").extract()).strip().replace(
            '\xa0', '.')
        items['telephone'] = base64.b64decode(
            response.xpath("//input[contains(@name, 'phoneBase64')]//@value").extract_first()).decode('utf-8')
        items['agency'] = 'IRR'
        yield items
