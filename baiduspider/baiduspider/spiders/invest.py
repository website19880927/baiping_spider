#!/usr/bin/env python
# encoding: utf-8
'''
@author: Ricardo
@license: (C) Copyright 2018-2019 @yang.com Corporation Limited.
@contact: 659706575@qq.com
@software: made@Yang
@file: invest.py
@time: 2018/9/6 0006 14:51
@desc:
'''

import scrapy
from baiduspider import items

class Invest(scrapy.Spider):
    name = 'invest'
    page=0
    def start_requests(self):
        # 产生urls  超过2000结束，网页中有
        while True:
            if self.page>2000:
                break
            else:
                url='https://www.vc.cn/investments?action=index&controller=investments&page='+str(self.page)+'&type=investment'

                yield scrapy.Request(url)

            self.page+=1


    def parse(self,response):
        # 获取网页中的字段，存入放到pipeline中返回
        try:
            websites=response.xpath('//div[@class="info"]/div[@class="name"]/a/@href')
            companies=response.xpath('//div[@class="info"]/div[@class="name"]/a/text()')
            industries=response.xpath('//div[@class="info"]/div[@class="taglist"]/span[1]/a/text()')
            cities=response.xpath('//div[@class="info"]/div[@class="taglist"]/span[2]/a/text()')
            rounds=response.xpath('//li[@class="round"]/a/text()')
            numbers=response.xpath('//td[@class="number"]/text()')
            angles=response.xpath('//td[@class="link-list"]/span/text()')
            times=response.xpath('//td[@class="invest-time"]/text()')
            for w,c,i,ci,ro,nu,an,ang in zip(websites,companies,industries,cities,rounds,numbers,angles,times):
                print(w.extract(),c.extract(),i.extract(),ci.extract(),ro.extract(),nu.extract(),an.extract(),ang.extract())
                web='https://www.vc.cn'
                website=web+w.extract()
                company=c.extract()
                industry=i.extract()
                city=ci.extract()
                round=ro.extract()
                number=nu.extract()
                angle=an.extract()
                time=ang.extract()
                item=items.IvestItem()
                item['website']=website
                item['company']=company
                item['industry']=industry
                item['city']=city
                item['round']=round
                item['number']=number
                item['angle']=angle
                item['time']=time
                yield item
        except Exception as a:
            print(a)
            pass







