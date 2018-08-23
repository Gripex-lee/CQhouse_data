# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from house_data.items import HouseDataItem

class CqhouseSpider(scrapy.Spider):
    name = 'CQhouse'
    allowed_domains = ['cq.lianjia.com']
    start_urls = ['https://cq.lianjia.com/ershoufang/pg1']

    def parse(self, response):
        for url in response.xpath('//div[@class="info clear"]/div[@class="title"]/a/@href').extract():
            yield Request(url=url,callback=self.detail_parse)

        for i in range(1,101):
            next_url = self.start_urls[0].replace("pg1","pg"+str(i))
            yield Request(url = next_url,callback=self.parse)

    def detail_parse(self,response):
        item = HouseDataItem()
        item["url"] = response.xpath('//div[@class="houseRecord"]/span[@class="info"]/text()').extract_first()
        item["price_per"] = response.xpath('//div[@class="unitPrice"]/span/text()').extract_first()
        item["price_total"] = response.xpath('//div[@class="price "]/span/text()').extract_first()
        item["room_number"] = re.findall(r"\d+",response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract_first())[0]
        item["living_room_number"] = re.findall(r"\d+",response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract_first())[1]
        item["high"] = re.findall(r"[\d.]+",response.xpath('//div[@class="room"]/div[@class="subInfo"]/text()').extract_first().split("/")[1])[0]
        item["house_toward"] = response.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()').extract_first()
        if re.findall(r".*?/.*?",response.xpath('//div[@class="type"]/div[@class="subInfo"]/text()').extract_first()):
            item["house_type"] = response.xpath('//div[@class="type"]/div[@class="subInfo"]/text()').extract_first().split("/")[1]
        else:
            item["house_type"] = response.xpath('//div[@class="type"]/div[@class="subInfo"]/text()').extract_first()
        
        item["size"] = re.findall(r"[\d.]+",response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').extract_first())[0]
        if re.findall(r"[\d.]+",response.xpath('//div[@class="area"]/div[@class="subInfo"]/text()').extract_first().split("/")[0]):
            item["build_year"] = re.findall(r"[\d.]+",response.xpath('//div[@class="area"]/div[@class="subInfo"]/text()').extract_first().split("/")[0])[0]
        else:
            item["build_year"] = "未知"
        
        item["buding_type"] = response.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()').extract_first()
        item["dianti"] = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()').extract_first()
        item["name"] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()').extract_first()
        item["location"] = response.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/a[1]/text()').extract_first()
        yield item
