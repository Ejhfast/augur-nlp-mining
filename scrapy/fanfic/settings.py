# Scrapy settings for fanfic project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'fanfic'

SPIDER_MODULES = ['fanfic.spiders']
NEWSPIDER_MODULE = 'fanfic.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fanfic (+http://www.yourdomain.com)'

AUTOTHROTTLE_ENABLED = True