# -*- coding:utf-8 -*-

import pymysql
import time

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "880818GD/",
    "db": "app_reviews_db",
    "charset": "utf8mb4",
}


class AppDAL():
    def insert_one_set(self, **kwargs):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO reviews_app(app_id,app_name,have_data,app_category,date_time) VALUES (%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql, (kwargs["app_id"], kwargs["app_name"], kwargs["have_data"],
                                         kwargs["app_category"], now))
        self.client.commit()
        self.client.close()

    # 根据app ID号查找在表中的序列号
    def query_one_set_by_id(self, app_id):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor()
        query_sql = "SELECT id FROM reviews_app WHERE app_id=%s"
        self.cursor.execute(query_sql, (app_id))
        result = self.cursor.fetchone()
        self.client.commit()
        self.client.close()
        return result


class ReviewsContentDAL():
    def insert_one_set(self, **kwargs):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO reviews_reviewscontent(review_content,review_version,review_rating,review_title,review_split,review_app_id_id,date_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql, (kwargs["review_content"], kwargs["review_version"], kwargs["review_rating"],
                                         kwargs["review_title"], kwargs["review_split"], kwargs["review_app_id_id"], now))
        self.client.commit()
        self.client.close()

    # 根据review_app_id_id号查找记录
    def query_one_set_by_id(self, review_app_id):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor(pymysql.cursors.DictCursor)
        query_sql = "SELECT * FROM reviews_reviewscontent WHERE review_app_id_id=%s"
        self.cursor.execute(query_sql, (review_app_id))
        result = self.cursor.fetchall()
        self.client.commit()
        self.client.close()
        return result

    # 根据review_app_id_id号,review_content查找记录
    def query_content_by_id(self, review_app_id, review_content):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor(pymysql.cursors.DictCursor)
        query_sql = "SELECT * FROM reviews_reviewscontent WHERE review_app_id_id=%s and review_content=%s"
        self.cursor.execute(query_sql, (review_app_id, review_content))
        result = self.cursor.fetchall()
        self.client.commit()
        self.client.close()
        return result

    # 查询所有还没分词的记录
    def query_all_not_split(self):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor(pymysql.cursors.DictCursor)
        query_sql = "SELECT * FROM reviews_reviewscontent WHERE review_split=%s"
        self.cursor.execute(query_sql, (0))
        result = self.cursor.fetchall()
        self.client.commit()
        self.client.close()
        return result

    # 更新分词状态
    def update_split_status(self, review_id):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor()
        update_sql = "UPDATE reviews_reviewscontent SET review_split=%s WHERE id=%s"
        result = self.cursor.execute(update_sql, (1, review_id))
        self.client.commit()
        self.client.close()


class SplitWordDAL():
    def insert_one_set(self, **kwargs):
        self.client = pymysql.connect(**MYSQL_CONFIG)
        self.cursor = self.client.cursor()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO reviews_splitwords(word,word_app_id_id,date_time) VALUES (%s,%s,%s)"
        self.cursor.execute(
            insert_sql, (kwargs["word"], kwargs["word_app_id_id"], now))
        self.client.commit()
        self.client.close()
