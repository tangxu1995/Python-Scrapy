# -*- coding: utf-8 -*-
from ..items import UserItem, UserRelationItem, WeiboItem, WeiboCommentItem, CommentReplyItem
import json
import scrapy


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']

    # 用户详情
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    # 关注页面
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 粉丝页面
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    # 博文页面
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    # 评论页面
    comment_url = 'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0'
    # 评论的回复
    comment_replyUrl = 'https://m.weibo.cn/comments/hotFlowChild?cid={comment_id}&max_id=0&max_id_type=0'

    start_users = ['1343887012', '3217179555', '1742566624', '2282991915', '1288739185', '3952070245', '5878659096']

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(url=self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """
        分析用户信息
        :param response: Response 对象
        """
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            field_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item

            # 关注
            uid = user_info.get('id')
            yield scrapy.Request(url=self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
                                 meta={'page': 1, 'uid': uid})

            # 粉丝
            yield scrapy.Request(url=self.fan_url.format(uid=uid, page=1), callback=self.parse_fans,
                                 meta={'page': 1, 'uid': uid})

            # 微博
            yield scrapy.Request(url=self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                                 meta={'page': 1, 'uid': uid})

    def parse_follows(self, response):
        """
        分析用户关注
        :param response: Response 对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) \
                and result.get('data').get('cards')[-1].get('card_group'):
            # 解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield scrapy.Request(url=self.user_url.format(uid=uid), callback=self.parse_user)

            # 关注列表
            uid = response.meta.get('uid')
            user_relation_item = UserRelationItem()
            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')}
                       for follow in follows]
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item

            # 下一页
            page = response.meta.get('page') + 1
            yield scrapy.Request(url=self.follow_url.format(uid=uid, page=page),
                                 callback=self.parse_follows, meta={'page': page, 'uid': uid})

    def parse_fans(self, response):
        """
        分析用户粉丝
        :param response: Response 对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get(
                        'card_group'):
            # 解析用户
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield scrapy.Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 粉丝列表
            user_relation_item = UserRelationItem()
            fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in
                    fans]
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item
            # 下一页粉丝
            page = response.meta.get('page') + 1
            yield scrapy.Request(self.fan_url.format(uid=uid, page=page),
                          callback=self.parse_fans, meta={'page': page, 'uid': uid})

    def parse_weibos(self, response):
        """
        分析微博列表
        :param response: Response 对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('ok') and result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_id = mblog.get('id')
                    yield scrapy.Request(url=self.comment_url.format(weibo_id=weibo_id),
                                          callback=self.parse_comments, meta={'weibo_id': weibo_id})

                    weibo_item = WeiboItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'created_at': 'created_at', 'reposts_count': 'reposts_count', 'picture': 'original_pic',
                        'pictures': 'pics', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic'
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')

                    yield weibo_item

                # 下一页
                uid = response.meta.get('uid')
                page = response.meta.get('page') + 1
                yield scrapy.Request(url=self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                                     meta={'uid': uid, 'page': page})

    def parse_comments(self, response):
        """
        分析某一条微博评论
        :param response: Response 对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('data'):
            comments = result.get('data').get('data')
            weibo_id = response.meta.get('weibo_id')
            for comment in comments:
                comment_item = WeiboCommentItem()
                field_map = {
                    'created_at': 'created_at', 'like_count': 'like_count', 'text': 'text'
                }
                for field, attr in field_map.items():
                    comment_item[field] = comment.get(attr)
                comment_id = comment.get('id')
                comment_item['weibo_id'] = weibo_id
                comment_item['comment_id'] = comment_id
                comment_item['user_id'] = comment.get('user').get('id')
                comment_item['user_name'] = comment.get('user').get('screen_name')
                yield comment_item

                max_id = result.get('data').get('max_id')

                yield scrapy.Request(url=self.comment_replyUrl.format(comment_id=comment_id),
                                     callback=self.parse_commentReply,
                                     meta={'weibo_id': weibo_id})

                yield scrapy.Request(url=self.comment_url.format(weibo_id=weibo_id)+'&max_id='+str(max_id),
                                     callback=self.parse_comments, meta={'weibo_id': weibo_id, 'max_id': max_id})

    def parse_commentReply(self, response):
        """
        分析某一条评论的回复
        :param response: Response 对象
        """
        weibo_id = response.meta.get('weibo_id')
        result = json.loads(response.text)
        if result.get('ok') and len(result.get('data')) != 0:
            replies = result.get('data')

            for reply in replies:
                created_at = reply.get('created_at')
                comment_id = reply.get('rootid')
                reply_id = reply.get('id')
                text = reply.get('text')
                user_id = reply.get('user').get('id')
                user_name = reply.get('user').get('screen_name')
                reply_original_text = reply.get('reply_original_text')
                like_count = reply.get('reply_original_text')
                reply_item = CommentReplyItem(weibo_id=weibo_id, created_at=created_at, comment_id=comment_id,
                                              reply_id=reply_id, text=text, user_id=user_id, user_name=user_name,
                                              reply_original_text=reply_original_text, like_count=like_count)
                yield reply_item

        # 查看评论的回复
        # https://m.weibo.cn/detail/{weibo_id}?cid={comment_id}


