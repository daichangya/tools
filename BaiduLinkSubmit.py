# -*- coding: utf-8 -*-
# Created by restran on 2017/4/26
from __future__ import unicode_literals, absolute_import
import requests
import xmltodict
import urllib

"""
主动推送站点链接到百度，读取 sitemap.xml
"""


class BaiduLinkSubmit(object):
    def __init__(self, site_domain, sitemap_url, baidu_token):
        self.site_domain = site_domain
        self.sitemap_url = sitemap_url
        self.baidu_token = baidu_token
        self.url_list = []

    def parse_sitemap(self):
        print('开始抓取sitemap')
        print('访问 %s' % self.sitemap_url)
        r = requests.get(self.sitemap_url)
        data = xmltodict.parse(r.text)
        self.url_list = [t['loc'] for t in data['urlset']['url']]
        print('抓取到%s项URL链接' % len(self.url_list))

    def submit(self):
        url22 = 'http://data.zz.baidu.com/urls?site=www.zthinker.com&token=W1gQAea8H0EEVlbQ'
        headers = {
            'Content-Type': 'text/plain'
        }
        url_list2 = list()
        for url in self.url_list:
            url = url.replace('https://zthinker.com/archives/','')
            url_list2.append('https://www.zthinker.com/archives/'+urllib.parse.quote(url))
        data = '\n'.join(url_list2)
        r = requests.post(url22, headers=headers, data=data)
        data = r.json()
        print('成功推送的url条数: %s' % data.get('success', 0))
        print('当天剩余的可推送url条数: %s' % data.get('remain', 0))
        not_same_site = data.get('not_same_site', [])
        not_valid = data.get('not_valid', [])
        if len(not_same_site) > 0:
            print('由于不是本站url而未处理的url列表')
            for t in not_same_site:
                print(t)

        if len(not_valid) > 0:
            print('不合法的url列表')
            for t in not_valid:
                print(t)


def main():
    # 需要修改为自己的域名
    site_domain = 'www.zthinker.com'
    # sitemap.xml 的地址
    sitemap_url = 'https://zthinker.com/sitemap.xml'
    # 在站长平台申请的推送用的准入密钥
    # 在百度站长平台可以查找到
    baidu_token = 'your_baidu_token'
    app = BaiduLinkSubmit(site_domain, sitemap_url, baidu_token)
    app.parse_sitemap()
    app.submit()


if __name__ == '__main__':
    main()