# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import pymysql


class LanrenAnchorsPipeline:

    def open_spider(self, spider):
        try:
            host = spider.settings.get('MYSQL_HOST')
            user = spider.settings.get('MYSQL_USER')
            password = spider.settings.get('MYSQL_PASSWORD')
            database = spider.settings.get('MYSQL_DATABASE')
            charset = spider.settings.get('MYSQL_CHARSET')
            spider.logger.info('open spider')
            # 连接数据库
            self.conn = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
            # 创建游标
            self.cursor = self.conn.cursor()
            spider.logger.info("start_time:{}".format(datetime.datetime.now()))
        except:
            self.open_spider(spider)
        else:
            spider.logger.info('MySQL:connected')

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
        spider.logger.info("end_time:{}".format(datetime.datetime.now()))
        spider.logger.info('close spider')

    def process_item(self, item, spider):
        spider.logger.info('anchor_name={}'.format(item['anchor_name']))

        sql = """insert into lanren_anchors(anchor_name,attention_nums,follower_nums,program_nums,anchor_addr,anchor_avatar)
                       values(%s,%s,%s,%s,%s,%s) on duplicate key update
                       anchor_name=values(anchor_name),
                       attention_nums=values(attention_nums),
                       follower_nums=values(follower_nums),
                       program_nums=values(program_nums),
                       anchor_addr=values(anchor_addr),
                       anchor_avatar=values(anchor_avatar)
                       """
        values = (item['anchor_name'], item['attention_nums'],
                  item['follower_nums'], item['program_nums'],
                  item['anchor_addr'], item['anchor_avatar'])

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            return item
        except Exception as e:
            spider.logger.info(repr(e))
            self.open_spider(spider)
