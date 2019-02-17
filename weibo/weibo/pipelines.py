# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import UserItem, WeiboItem, UserRelationItem, WeiboCommentItem, CommentReplyItem
from pymongo.errors import DuplicateKeyError


class WeiboPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['weibo']
        self.userInfos = self.db['users']
        self.weibos = self.db['weibos']
        self.userRelations = self.db['userRelations']
        self.comments = self.db['comments']
        self.commentReply = self.db['commentReplies']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if isinstance(item, UserItem):
            self.insert_item(self.userInfos, item)

        elif isinstance(item, WeiboItem):
            self.insert_item(self.weibos, item)

        elif isinstance(item, UserRelationItem):
            self.insert_item(self.userRelations, item)

        elif isinstance(item, WeiboCommentItem):
            self.insert_item(self.comments, item)

        elif isinstance(item, CommentReplyItem):
            self.insert_item(self.commentReply, item)

        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass

