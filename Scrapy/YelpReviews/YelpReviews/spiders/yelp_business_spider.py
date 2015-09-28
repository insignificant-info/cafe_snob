import sys
import scrapy
import pickle
from scrapy.selector import Selector
from scrapy.http import Request

'''
Uses output of YelpCoffeeReviews aka yelp_spider (which produces a list of urls to scrape). That output is cleaned and saved as a pickle file which is hardcoded below. Call by navigating to YelpReviews then use:
    
    scrapy crawl yelpReview -o output.json -t jsonlines


'''

from YelpReviews.items import YelpreviewsItem


class YelpReviewSpider(scrapy.Spider):
    name = "yelpReview"
    allowed_domains = ["yelp.com"]

    location_strings = pickle.load( open( "/Users/Paul/Dropbox/Projects/Insight/Cafe_Snob/cafe_snob/Scrapy/review_urls_to_scrape.pkl", "rb" ) )
    start_urls = []
    for location in location_strings:
        
        start_urls.append("http://www.yelp.com/" + location + "?start=0")

    start_urls = start_urls#[0:50]


    def parse(self, response):
        total_results = response.xpath('//span[@itemprop="reviewCount"]/text()').extract()
        # if the biz has no reviews then total_results will return an empty list. 
        # if there are no reviews then skip the while loop by setting i to -1

        if not total_results:
            total_results = -1
        else:
            total_results = total_results[0].split()
        # Grab the last item
            total_results = int(total_results[-1])


        
        i=0
        while i <  total_results:
            url = response.request.url
            url = url + "?start=" + str(i)
            print(url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)
            i = i+40

    def parse_dir_contents(self, response):
        item = YelpreviewsItem()
        sel = Selector(response)
        reviews = sel.xpath('//div[@class="review review--with-sidebar"]')
        items = []

        for review in reviews:
            item = YelpreviewsItem()
            biz_name_temp = response.xpath(".//h1[@itemprop='name']/text()").extract()
            item["biz_name"] = ' '.join(biz_name_temp[0].split())
            item["biz_id"] = response.xpath('.//meta[@name="yelp-biz-id"]/@content').extract()
            biz_hood_temp = response.xpath('.//span[@class="neighborhood-str-list"]/text()').extract()
            try:
                item["biz_hood"] = ' '.join(biz_hood_temp[0].split())
            except:
                item["biz_hood"] = biz_hood_temp
            item['reviewer_name'] = review.xpath('.//li[@class="user-name"]/a/text()').extract()
            item["reviewer_id"] = review.xpath('.//li[@class="user-name"]/a/@href').extract()
            item['review_rating'] = review.xpath('.//meta[@itemprop="ratingValue"]/@content').extract()
            item['review_date'] = review.xpath('.//meta[@itemprop="datePublished"]/@content').extract()
            item['review_text'] = review.xpath('.//p[@itemprop="description"]/text()').extract()
            item['url'] = response.url

            item['rating'] = response.xpath('.//div[@itemprop="aggregateRating"]//meta[@itemprop="ratingValue"]/@content').extract()
            item['price_rating'] = response.xpath('.//span[@itemprop="priceRange"]/text()').extract()
            item['review_count'] = response.xpath('.//div[@itemprop="aggregateRating"]//span[@itemprop="reviewCount"]/text()').extract()

            ''' Here are some extra Xpaths that I don't have the heart to delete yet
            # response.xpath('.//dt[@class="attribute-key"]/text()').extract()

            #  test = response.xpath('.//div[@class="short-def-list"]/dl')
            # test[1].xpath('.//dt[@class="attribute-key"]/text()').extract()
            # test[1].xpath('.//dd/text()').extract() '''

            attributes = response.xpath('.//div[@class="short-def-list"]/dl')
            row = {}
            for attribute in attributes:
                label_temp = attribute.xpath('.//dt[@class="attribute-key"]/text()').extract()
                label = '_'.join(label_temp[0].split())
                label = label.replace('-','_').lower()
                value_temp = attribute.xpath('.//dd/text()').extract()
                row[label] = ' '.join(value_temp[0].split())
            item['attributes'] = row

            yield item





        

        # review_count = response.xpath("//span[@class='review-count rating-qualifier']/text()").extract()
        # review_count_list = []
        # for single in review_count:
        #   single_count = single.split()
        #   review_count_list.append(int(single_count[0]))
        # #for some reason it is pulling in a "27" as the first item for review counts. After the 27 are the 10 numbers I would expect. Just droping the first number for now.
        # item["biz_review_count"] = review_count_list #[1:]





        # item = YelpcoffeereviewsItem()
        # item["biz_url"] = response.xpath("//span[@class='indexed-biz-name']/a[@class='biz-name']/@href").extract()
        # yield item
