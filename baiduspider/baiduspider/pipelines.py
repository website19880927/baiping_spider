# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import time

import happybase


class BaiduspiderPipeline(object):
    def process_item(self, item, spider):

        city = item['city']
        title = item['title']
        salary = item['salary']
        company = item['company']
        job = item['job']
        uptime = item['uptime']
        exper = item['exper']
        edu = item['edu']
        loc = item['loc']
        host=item['host']
        times = time.asctime()
        status = 1
        brief_company = item['brief_company']
        db = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='crawler',
            charset='utf8'
        )
        cursor = db.cursor()
        # sql='count(*) from t_zhilian'
        cursor.execute('select count(*) from t_zhilian')
        num=cursor.fetchone()[0]
        cursor.close()
        print('@pipeline在mysql的条数目前有',num)
        if num<100:
            cursor = db.cursor()
            sql = 'insert into t_zhilian(city,title,salary,company,job,uptime,exper,edu,loc,brief_company,host,times,status )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
            # print(city,title,salary,company,job,uptime,exper,edu,loc,brief_company)
                cursor.execute(sql,[city,title,salary,company,job,uptime,exper,edu,loc,brief_company,host,times,status])
                db.commit()
                print('inset@@@@@@@@@@@@@48')
                cursor.close()
            except:
                db.rollback()
            db.close()
        else:
            print('@pipeline 进入 hbase',item)
            connection = happybase.Connection(host="192.168.43.188", port=9090)
            connection.open()
            # families={
            #     'position': dict(),
            #     'company_info': dict()
            #
            # }
            # connection.create_table('crawler:t_zhilian',families)
            table = connection.table('crawler:t_zhilian')


            table.put(city+title+host+company, {'position:title': title})
            table.put(city+title+host+company, {'position:salary': salary})
            table.put(city+title+host+company, {'position:exper': exper})
            table.put(city+title+host+company, {'position:edu': edu})
            table.put(city+title+host+company, {'position:company': company})
            table.put(city+title+host+company, {'position:job': job})

            table.put(city+title+host+company, {'company_info:loc': loc})
            table.put(city+title+host+company, {'company_info:brief_company':brief_company})



        return item


class InvestPipeline(object):
    def process_item(self, item, spider):
        # 将数据通过管道传到数据库中
        website = item['website']
        company = item['company']
        industry = item['industry']
        city = item['city']
        round = item['round']
        number = item['number']
        angle = item['angle']
        time = item['time']
        db = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='crawler',
            charset='utf8'
        )
        cursor = db.cursor()
        sql = 'insert into t_invest(website,company,industry,city,round,number,angle,time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,[website,company,industry,city,round,number,angle,time])
            db.commit()
            print('inset@@@@@@@@@@@@@数据库存储中',website,company,industry,city,round,number,angle,time)
            cursor.close()
        except:
            db.rollback()
        db.close()