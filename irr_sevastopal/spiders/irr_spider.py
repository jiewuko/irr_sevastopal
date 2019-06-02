import base64

import scrapy
from items import IrrSevastopalItem


class IrrSpider(scrapy.Spider):
    name = 'IrrSpider'
    allowed_domains = ['sevastopol.irr.ru']

    def start_requests(self):
        yield scrapy.Request(
            url='https://sevastopol.irr.ru/real-estate/out-of-town/lands/sevastopol-gorod/',
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
                yield scrapy.Request(url='https://sevastopol.irr.ru' + pagination_url,
                                     callback=self.parse)

    def parse_announcement(self, response):
        items = IrrSevastopalItem()
        items['url'] = response.url
        items['name'] = response.xpath("//h1/text()").extract_first().strip()
        items['decription'] = ' '.join(''.join(response.xpath(
            "//p[contains(@itemprop, 'description')]//text()").extract()).strip().replace('\n', '').split())
        items['subcategory'] = ' '.join(''.join(response.xpath(
            "//li[contains(@itemprop, 'itemListElement')]//a//text()").extract()).split())
        items['address'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__infoTextBold js-scrollToMap')]//text()").extract()).strip()
        items['published_date'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__createDate')]//text()").extract()).strip()
        items['price'] = ''.join(response.xpath(
            "//div[contains(@class, 'productPage__price js-contentPrice')]//text()").extract()).strip().replace(
            '\xa0', '.')
        items['telephone'] = base64.b64decode(
            response.xpath("//input[contains(@name, 'phoneBase64')]//@value").extract_first()).decode('utf-8')
        yield items
