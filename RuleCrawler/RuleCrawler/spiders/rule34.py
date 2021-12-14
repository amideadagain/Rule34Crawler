from scrapy import Spider, Request
from ..items import RulecrawlerItem


class RuleSpider(Spider):
    name = 'pics'
    base_url = 'https://rule34.xxx/'
    start_urls = [
        'https://rule34.xxx/index.php?page=post&s=list&tags=erere+'
    ]

    def parse(self, response):
        for img_page in response.css("div.content span.thumb a::attr(href)"):
            page_link = self.base_url + img_page.get()
            yield Request(page_link, callback=self.parse_pages)

        next_page_url = response.xpath("//div[@class='pagination']//a[@alt='next']/@href").extract_first()
        if next_page_url is not None:
            yield Request(response.urljoin(next_page_url))

    def parse_pages(self, response):
        img_link = response.xpath("//meta[@property='og:image' and @itemprop='image']/@content").extract_first()

        rule_item = RulecrawlerItem()
        rule_item['image_urls'] = img_link

        yield rule_item
