import scrapy
import json
from scrapy.http import Request
from WallmartSpider.items import WallmartspiderItem


headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,ml;q=0.8,hi;q=0.7',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

class wallmartspider(scrapy.Spider):
	name="wallmartspider"
	handle_httstatus_list=[500]

	

	def start_requests(self):
		for i in range(0,26):
			url="https://www.walmart.com/search/?cat_id=0&grid=true&page="+str(i)+"&ps=40&query=bikes#searchProductResult"
			yield Request(url, headers=headers, callback=self.search_page)

	def search_page(self,response):
		page_urls = response.xpath('//script[@id="searchContent"]/text()').extract()
		jscontent=json.loads("".join(response.xpath('//script[@id="searchContent"]/text()').extract())) 
		productList=jscontent['searchContent']['preso']['items'] 
		for i in range(len(productList)):
			productPageUrl=productList[i]['productPageUrl']
			yield Request(response.urljoin(productPageUrl), headers=headers, callback=self.product_page)




	def product_page(self,response):

		items=WallmartspiderItem()
		items['title']=response.xpath('//h1//text()').extract_first()
		items['currentPrice']=response.xpath('//span[@class="price-group"]//@aria-label').extract_first()
		items['oldPrice']=response.xpath('//div[contains(@class,"price-old display-inline")]//span[@class="price-group"]//@aria-label').extract_first()
		items['userRating']= response.xpath('//div[@class="ReviewsHeader-ratingContainer"]//text()').extract_first() 
		items['aboutItem']=("".join(response.xpath('//div[@class="product-about"]//text()').extract())).replace('\n','').replace('\''," '")
		
		
		specifications={}
		specificationsTable=response.xpath('//table[contains(@class, "specification")]//tr')
		for i in specificationsTable:
			key = i.xpath('td[@class="display-name"]/text()').extract_first('') 
			value = i.xpath('td/div/text()').extract_first('')
			specifications[key]=value

		items["specifications"]=specifications

		yield items


