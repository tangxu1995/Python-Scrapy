# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64

""" 阿布云ip代理配置，包括账号密码 """
proxyServer = "http://http-dyn.abuyun.com:9020"
proxyUser = "H2NV8EPL3RKF1TID"
proxyPass = "286DB6D840A834C0"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ABProxyMiddleware(object):
    """ 阿布云ip代理配置 """
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth

class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


COOKIES = {
    '_T_WM=e97988a9362c7edadcfab10bebda8a05; SCF=Ap3iFbcxuRA4yW9U65mPwzYzKk1XqlG0WoAJNTC-cg2N7Yte9nq3jqlsqIjyUU1mhMFOh8OuhBU02vXzmMNr7Rs.; XSRF-TOKEN=80328a; M_WEIBOCN_PARAMS=oid%3D3700437129275811%26luicode%3D10000011%26lfid%3D2304136982447978_-_WEIBO_SECOND_PROFILE_WEIBO; MLOGIN=0; SUB=_2A25xbKYkDeRhGeBH41AV8yfPwjWIHXVSrspsrDV6PUJbkdAKLRnskW1NQb4Pq2Yxfpfqk1nNZrVZ-qI9joDnvREC; SUHB=0N2lNp4hUpc2tE; SSOLoginState=1550374516',
    '_T_WM=e97988a9362c7edadcfab10bebda8a05; SCF=Ap3iFbcxuRA4yW9U65mPwzYzKk1XqlG0WoAJNTC-cg2N7Yte9nq3jqlsqIjyUU1mhMFOh8OuhBU02vXzmMNr7Rs.; XSRF-TOKEN=80328a; M_WEIBOCN_PARAMS=oid%3D3700437129275811%26luicode%3D10000011%26lfid%3D2304136982447978_-_WEIBO_SECOND_PROFILE_WEIBO; MLOGIN=0; SUB=_2A25xbKXEDeRhGeBH41EQ8S7EzT-IHXVSrsuMrDV6PUJbkdANLRT5kW1NQb4Pnl5upYbLb3JQmuZA9B5PfXNOp00q; SUHB=0QSpBlY0Ciya0F; SSOLoginState=1550374292',
    '_T_WM=e97988a9362c7edadcfab10bebda8a05; XSRF-TOKEN=088029; WEIBOCN_FROM=1110106030; SCF=Ap3iFbcxuRA4yW9U65mPwzYzKk1XqlG0WoAJNTC-cg2N7Yte9nq3jqlsqIjyUU1mhMFOh8OuhBU02vXzmMNr7Rs.; SUB=_2A25xY4oIDeRhGeBJ7FEQ8SbMzDqIHXVSrxZArDV6PUJbktAKLWygkW1NRi0_2EiKu3xWhgxALMP4_8SjhsSVP9Nd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhUSdihWYcW7M.8L3vYOC4i5JpX5KzhUgL.FoqNS0epeKn7S0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcS0M0eK2RehMc; SUHB=0k1SuISsgC58HP; SSOLoginState=1550318168; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D3700437129275811%26luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174',
}