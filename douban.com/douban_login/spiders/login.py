# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import requests
from urllib import request
from hashlib import md5
from PIL import Image


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/people/189512220/']
    edit_signature_url = 'https://www.douban.com/j/people/189512220/edit_signature'
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }

    def parse(self ,response):
        if response.url == 'https://www.douban.com/people/189512220/':
            print('-----已经进入个人详情页-----')
            print('-----正在修改个人签名-----')
            ck = response.xpath("//*[@id='edit_signature']/form/div/input/@value").get()
            data = {
                'ck': ck,
                'signature': '我可以自动识别验证码啦~~'
            }
            yield FormRequest(self.edit_signature_url, formdata=data, callback=self.success)

    def success(self, response):
        print('-----个人签名修改成功-----')


    # 模拟登录
    login_url = 'https://accounts.douban.com/login'
    def start_requests(self):
        yield Request(self.login_url, callback=self.login)


    def login(self, response):
        print('-----登录程序-----')
        captcha_id = response.xpath(".//input[@name='captcha-id']/@value").get()
        captcha_url = response.xpath("//*[@id='captcha_image']/@src").get()
        if captcha_url is None:
            print('-----登录时无验证码-----')
            data = {
                'form_email': '871117040@qq.com',
                'form_password': 'tx211314'
            }
        else:
            print('-----登录时有验证码-----')
            print('-----即将下载验证码-----')
            request.urlretrieve(captcha_url, 'captcha.png',)
            image = Image.open('captcha.png')
            image.show()
            captcha_solution = input("请输入验证码:")
            # captcha_solution = self.recognize_captcha('captcha.png')
            data = {
                'form_email': '871117040@qq.com',
                'form_password': 'tx211314',
                'captcha-solution': captcha_solution,
                'captcha-id': captcha_id,
                'login': '登录'
            }
        print('-----登录中-----')
        yield FormRequest.from_response(response, formdata=data, callback=self.parse_after_login)


    def parse_after_login(self, response):
        if "笑谈一纸风华的帐号" in response.text:
            print('-----登录成功-----')
            yield from super().start_requests()


    def recognize_captcha(self, im):
        print('-----正在进行验证码识别-----')
        username = 'tangxu1995'
        password = 'a211314'.encode('utf-8')
        password = md5(password).hexdigest()
        soft_id = '898320'
        base_params = {
            'user': username,
            'pass2': password,
            'softid': soft_id
        }

        codetype = '1007'
        params = {
            'codetype': codetype
        }
        params.update(base_params)

        im = open(im, 'rb').read()
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        captcha = r.json()['pic_str']
        print('-----验证码识别完毕-----')
        print('验证码为：%s' % captcha)
        return captcha
