import sys
import scrapy
import pickle

from YelpCoffeeReviews.items import YelpBusinessItem

'''
This spider grabs the urls for all cafes/cofee shops in a city by scraping Yelp. It requires a list of all the neighborhoods in a city which also must be scraped from yelp. That list can be collected by navigating to a yelp search page in the target city which has the option to filter by neighborhoods. Open that page in the scrapy command line then use:

save_variable = response.xpath('.//label[@class = "place radio-check"]/input/@value').extract()

to grab all of the nieghborhoods. They should be in the form like IL:Chicago::West_Lawn or NY:New_York:Brooklyn:Gowanus.

Then save it with:

import pickle
pickle.dump(save_variable,open("city_locations.pkl","wb"))


The output can be used to feed the second spider (yelp_business_spider... sorry about the names) which then goes to all of these found URLs and grabs reviews + business data. Currently I load a pickle file of saved NYC locations, but that should be replaced with pulling in a simple csv.

Before the output can be used in yelp_business_spider it first must be run throught scraped_names_to_urls.py

'''

class YelpSpider(scrapy.Spider):
	name = "yelp"
	allowed_domains = ["yelp.com"]
    # start_urls = ["http://www.yelp.com/search?find_loc=New+York,+NY,+USA&start=0&cflt=coffee"]
	location_strings = pickle.load( open( "saved_locations.p", "rb" ) )
	location_split = [strings.split(':') for strings in location_strings]
	start_urls = []
	for location in location_split:

		# Note, modified this to change NY at the end to location[0]. confirm that that works
		start_urls.append("http://www.yelp.com/search?cflt=coffee&find_loc=" + location[3] +",+" +location[2]+ ",+"+location[0]+"&start=0")
		start_urls.append("http://www.yelp.com/search?cflt=cafes&find_loc=" + location[3] +",+" +location[2]+ ",+"+location[0]+"&start=0")




	start_urls = start_urls
 	

	def parse(self, response):
		total_results = response.xpath("//span[@class='pagination-results-window']/text()").extract()
		total_results = total_results[0].split()
		total_results = int(total_results[-1])


		
		i=0
		while (i <  total_results) and (i < 1000):
			
			url = response.request.url
			url = url[:-1] + str(i)
			print(url)
			yield scrapy.Request(url, callback=self.parse_dir_contents)
			i = i+10

	def parse_dir_contents(self, response):
		item = YelpBusinessItem()
		item["biz_url"] = response.xpath("//span[@class='indexed-biz-name']/a[@class='biz-name']/@href").extract()
		item["biz_name"] = response.xpath("//span[@class='indexed-biz-name']/a[@class='biz-name']/text()").extract()


		'''If i decide to scrape more cleanly and pul in one business at a time instead of list of 10 then use:
		#results = response.xpath("//span[@class='indexed-biz-name']/a[@class='biz-name']")
		for result in results:
		item["biz_url"] = results[1].xpath("@href").extract()
		#results[1].xpath("text()").extract() should grab the name but only gets first word right now so would take some cleaning up

		results[1].xpath("@href").extract()

		review_count = response.xpath("//span[@class='review-count rating-qualifier']/text()").extract()
		review_count_list = [] '''



		yield item



