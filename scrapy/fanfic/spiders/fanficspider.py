from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from fanfic.items import FanficPage

class FanficSpider(Spider):
    name = "fanfic"
    allowed_domains = ["fanfiction.net"]
    start_urls = [
        "https://www.fanfiction.net/tv/Glee/"
    ]

    def parse(self, response):
        select = Selector(response)
        stories = select.css('a.stitle')
        for story in stories.xpath('@href').extract():
            url = 'https://www.fanfiction.net' + story
            yield Request(url, self.parseStoryPage)

        # index next page too
        next_page = select.xpath('//a[contains(text(), "Next")]/@href')
        if len(next_page) > 0:
            next_page_url = next_page[0].extract()
            yield Request('https://www.fanfiction.net' + next_page_url, callback=self.parse)


    def parseStoryPage(self, response):
        select = Selector(response)
        textnodes = select.css('.storytext p').xpath('text()')
        language = ' '.join(select.css('#profile_top .xgray').xpath('text()').extract())

        if 'English' in language and len(textnodes) >= 1:
            front = response.url.split("/")[:-3]
            story_id = int(response.url.split("/")[-3])
            page_num = int(response.url.split("/")[-2])
            end = response.url.split("/")[-1:]

            text = textnodes.extract()
            page = FanficPage()
            page['text'] = u'\n'.join(text)
            with open('stories/' + str(story_id) + '.txt', 'a') as txtfile:
                unicode_text = (page['text'] + u'\n').encode('utf8')
                txtfile.write(unicode_text)

            # crawl the next page
            yield Request('/'.join(front) + '/' + str(story_id) + '/' + str(page_num+1) + '/' + '/'.join(end), callback=self.parseStoryPage)

