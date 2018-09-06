#!/usr/bin/env python
# encoding: utf-8
'''
@author: Ricardo
@license: (C) Copyright 2018-2019 @yang.com Corporation Limited.
@contact: 659706575@qq.com
@software: made@Yang
@file: baiping.py
@time: 2018/9/5 0005 23:46
@desc:
'''

import json
from urllib import parse
from baiduspider import items
import scrapy

class Baidu(scrapy.Spider):
    name = 'baidu'
    city = [parse.quote('北京'), parse.quote('上海'), parse.quote('广州'), parse.quote('深圳')]
    key = [parse.quote('大数据'), 'AI', parse.quote('爬虫'), 'python']
    city_index = 0
    key_index = 0
    pn=0

    def start_requests(self):
        # 这里 产生新的url 不停的产生 ，解析百度招聘中的对应信息，
        while True:

            url = 'http://zhaopin.baidu.com/api/qzasync?city=' + self.city[self.city_index] + '&pcmod=1&pn=' + str(
                self.pn) + '&rn=10' + '&query=' + self.key[self.key_index]

            yield scrapy.Request(url, callback=self.get_urls)
            self.pn += 10

            print('generating......', url)

            # yield scrapy.Request(url,callback=self.get_urls)
                # yield scrapy.Request('http://zhaopin.baidu.com/api/qzasync?query=AI&city=%25E5%258C%2597%25E4%25BA%25AC&pcmod=1&pn=10&rn=10',callback=self.get_urls)

    def get_urls(self,response):
    # 由于返回的是json,因此解析，找到对应的字段，拼接新的url，详情页的url，需要对页面num判断，这里不熟悉 线程的开启，是否影响条件的切换。
     # 同时产生的多个进程，pn 一旦超过界限，后面的pn 归零，但是之前是否产生多个大于num的 还没有判断，一旦没有判断，key_index 就不停加，一下子就满了，报错。。。
        print('adadad',response.text)
        back=json.loads(response.text)
        try:
            self.num=back['data']['dispNum']
        except:
            pass
        if int(self.num)<self.pn:
            print(self.key_index, self.pn,'   e')
            title=back['data']['hilight']

            print(title, len(title))
            title=parse.quote(title)

            for i in back['data']['disp_data']:
                resource = i['loc']
                m=''
                for j in resource:
                    m+=parse.quote(j)
                resource = m.replace('/', '%2F')
                print(i['city'],resource)
                city=parse.quote(i['city'])

                url='http://zhaopin.baidu.com/szzw?id='+resource+'&query='+title+'&city='+city
                print('新的url详情页',url)
                yield scrapy.Request(url)
        else:
            self.key_index += 1
            self.pn = 0
        if self.key_index >= len(self.key):
            self.city_index += 1
            self.key_index = 0
            self.pn = 0
        if self.city_index >= len(self.city):
            print('循环结束，没有城市了。。。。。。')


    def parse(self, response):
        title=response.xpath('//h4/text()')[0].extract()
        salary=response.xpath('//div[@class="salary-container"]/span[@class="salary"]/text()')[0].extract()
        edu=response.xpath('//div[@class="job-require"]/text()')[0].extract()
        exper=response.xpath('//div[@class="job-require"]/text()')[1].extract()
        up_time=response.xpath('//div[@class="job-classfiy"]/p/text()')[2].extract()
        city=response.xpath('//div[@class="job-classfiy"]/p/text()')[-1].extract()
        job=response.xpath('//div[@class="job-detail"]/p/text()')[0].extract()
        loc=response.xpath('//div[@class="job-addr"]/p[2]/text()')[0].extract()
        company=response.xpath('//div[@class="item-bd"]/h4/text()')[0].extract()
        company1=response.xpath('//div[@class="title-box clearfix"]/p[@class="more"]/a/@href')[0].extract()
        brief_company='http://zhaopin.baidu.com'+company1
        item = items.ZhilianItem()
        item['title'] = title
        item['salary'] = salary
        item['company'] = company
        item['job'] = job
        item['uptime'] = up_time
        item['exper'] = exper
        item['edu'] = edu
        item['loc'] = loc
        item['brief_company'] = brief_company
        item['city'] = city
        item['host'] = 'baiping'
        print('@77目前进行的是百度招聘', city,title)
        yield item






