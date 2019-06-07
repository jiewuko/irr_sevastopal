# -*- coding: utf-8 -*-

# Scrapy settings for irr_sevastopal project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'irr_sevastopal'

SPIDER_MODULES = ['irr_sevastopal.spiders']
NEWSPIDER_MODULE = 'irr_sevastopal.spiders'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'irr_sevastopal (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'irr_sevastopal.middlewares.IrrSevastopalSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'irr_sevastopal.middlewares.IrrSevastopalDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'irr_sevastopal.pipelines.SQLiteStorePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


FEED_EXPORTERS = {
    'xlsx': 'irr_sevastopal.exporter.ExcelItemExporter'
}

FIELDS_TO_EXPORT = [
    'url', 'name', 'description', 'subcategory', 'address', 'published_date', 'price', 'telephone', 'agency',
]

# LOG_LEVEL = 'INFO'

RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}

data = {
    'Категория':
    {
        'Жилая недвижимость': {
            'Тип': {
                'Продажа': {
                    'Студии': 'apartments-sale/studio/',
                    '1-комнатные квартиры': 'apartments-sale/one-rooms/',
                    '2-комнатные квартиры': 'apartments-sale/two-rooms/',
                    '3-комнатные квартиры': 'apartments-sale/three-rooms/',
                    'Многокомнатные квартиры': 'apartments-sale/multiroom/',
                    'Все квартиры': 'apartments-sale/',
                    'Комнаты': 'rooms-sale/',
                    'Вторичное жилье': 'apartments-sale/secondary/',
                    'Новостройки': 'apartments-sale/new/',
                    'Сданные новостройки': 'apartments-sale/new/sdan/',
                },
                'Аренда': {
                    'Студии': 'rent/studio/',
                    '1-комнатные квартиры': 'rent/one-rooms/',
                    '2-комнатные квартиры': 'rent/two-rooms/',
                    '3-комнатные квартиры': 'three-rooms/',
                    'Многокомнатные квартиры': 'rent/multiroom/',
                    'Все квартиры': 'rent/',
                    'Комнаты': 'rooms-rent/',
                    'Дома': 'out-of-town-rent/houses/',
                },
            }
        },
        'Коммерческая недвижимость': {
            'Тип': {
                'Продажа': {
                    'Офисы': 'commercial-sale/offices/',
                    'Производство и склады': 'commercial-sale/production-warehouses/',
                    'Здания и особняки': 'commercial-sale/houses/',
                    'Торговля и сервис': 'commercial-sale/retail/',
                    'Кафе. Бары. Рестораны': 'commercial-sale/eating/',
                    'Другого и свободного назначения': 'commercial-sale/misc/',
                },
                'Аренда': {
                    'Офисы': 'commercial/offices/',
                    'Производство и склады': 'commercial/production-warehouses/',
                    'Здания и особняки': 'commercial/houses/',
                    'Торговля и сервис': 'commercial/retail/',
                    'Кафе. Бары. Рестораны': 'commercial/eating/',
                    'Другого и свободного назначения': 'commercial/misc/',
                },
            }
        },
        'Дома, дачи, участки': {
            'Тип': {
                'Продажа': {
                    'Дома': 'out-of-town/houses/',
                    'Таунхаусы': 'out-of-town/townhouses/',
                    'Дачи': 'out-of-town/country-houses/',
                    'Участки': 'out-of-town/lands/',
                },
                'Аренда': {
                    'Дома': 'out-of-town-rent/houses/',
                    'Таунхаусы': 'out-of-town-rent/townhouses/',
                    'Участки': 'out-of-town-rent/lands/',
                },
            }
        },
    }
}

CATEGORY = 'Коммерческая недвижимость'
TYPE_ = 'Продажа'
SUB_CATEGORY = 'Офисы'

URL = data.get('Категория').get(CATEGORY).get('Тип').get(TYPE_).get(SUB_CATEGORY)

