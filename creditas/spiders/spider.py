import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CreditasItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class CreditasSpider(scrapy.Spider):
	name = 'creditas'
	start_urls = ['https://www.creditas.cz/ze-zivota-banky/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="c-article__item col-md-8 offset-md-2"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//div[@class="c-article-detail__article"]/text()').get()
		title = response.xpath('//h1[@class="c-article-detail__title"]/text()').get()
		content = response.xpath('//div[@class="c-article-detail__perex"]//text()').getall() + response.xpath('//div[@class="c-article-detail__text"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=CreditasItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
