# -*- coding: utf-8 -*-
import scrapy

class UkdirectorySpider(scrapy.Spider):
    name = 'ukdirectory'
    allowed_domains = ['ukdirectory.co.uk']
    start_urls = ['https://www.ukdirectory.co.uk/manufacturing-and-industry/manufacturing/']


    def parse(self, response):
    	links = response.css('li h3 a::attr(href)').extract()

    	i = 0

    	for link in links:
    		get_link = response.urljoin(link)

    		i+= 1

    		yield scrapy.Request(get_link, callback=self.parse_p )


    def parse_p(self, response):
    	links = response.css('.directory-listing h3 a::attr(href)').extract()

    	counts = len(links)
    	counts = str(counts)

    	print ('Total Sub link '+counts)
    	print ('\n')

    	i = 0

    	for link in links:
    		get_link = response.urljoin(link)

    		i+= 1

    		yield scrapy.Request(get_link, callback=self.parse_p2 )

    	next_pages = response.css('a.more::attr(href)').extract_first()

    	if next_pages:
    		next_page = response.urljoin(next_pages)

    		yield scrapy.Request(next_page, callback=self.parse_p )


    def parse_p2(self, response):

        url = response.url
        
        category = response.xpath('//*[@title="Description"]//text()')
        if category:
            category = category.extract()[-1].strip()

        name = response.xpath('//*[@class="title"]//text()')
        if name:
        	name = name.extract()[-1].strip()

        contact = response.css('div#pn::text').extract_first().strip()

        location = response.css('address::text').extract()
        location = [node.replace('\n', '') for node in location]
        location = [node.strip() for node in location]
        location = filter(None, location)
        location = ' '.join(location)

        yield {
        	'url':url,
        	'category':category,
        	'name':name,
        	'contact':contact,
        	'location':location

        }




