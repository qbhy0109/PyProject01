"""import requests
from lxml import etree

headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
    'Referer': 'http://www.xbiquge.la/7/7931',
    'Cookie': 'Hm_lvt_169609146ffe5972484b0957bd1b46d6=1632658407; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1632658407',
    'Accept-Encoding': 'gzip. deflate'
}


# 获取网站源码
def get_text(url, headers):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 获取小说信息
def get_novelinfo(list1, name_list):
    for i, url in enumerate(list1):
        html = etree.HTML(get_text(url, headers))
        name = name_list[i]
        title_url = html.xpath('//div[@id="list"]/dl/dd/a/@href')
        title_url = ['http://www.xbiquge.la' + i for i in title_url]     # 章节地址
        titlename_list = html.xpath('//div[@id="list"]/dl/dd/a/text()')  # 章节名字列表
        get_content(title_url, titlename_list, name)


# 获取小说每章节内容
def get_content(url_list, title_list, name):
    for i, url in enumerate(url_list):
        item = {}
        html = etree.HTML(get_text(url, headers))
        content_list = html.xpath('//div[@id="content"]/text()')
        content = ''.join(content_list)
        content = content + '\n'
        item['title'] = title_list[i]
        item['content'] = content.replace('\r\r', '\n').replace('\xa0',' ')
        print(item)
        with open(name + '.txt', 'a+', encoding='utf-8') as file:
            file.write(item['title'] + '\n')
            file.write(item['content'])


def main():
    base_url = 'http:www.xbiquge.la/xiaoshuodaquan/'
    html = etree.HTML(get_text(base_url, headers))
    novelurl_list = html.xpath('//div[@class="novellist"]/ul/li/a/@href')
    name_list = html.xpath('//div[@class="novellist"]/ul/li/a/text()')
    get_novelinfo(novelurl_list, name_list)


if __name__ == '__main__':
    main()


"""

import requests
from lxml import etree
from BQG_try1 import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Referer': 'http://www.xbiquge.la/7/7931/',
    'Cookie': '_abcde_qweasd=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=jUBgtRGIR19uAr-RE9YV9eHokjmGaII9Ivfp8FJIwV7&wd=&eqid=9ecb04b9000cdd69000000035dc3f80e; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1573124137; _abcde_qweasd=0; bdshare_firstime=1573124137783; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1573125463',
    'Accept-Encoding': 'gzip, deflate'
}


# 获取网站源码
def get_text(url, headers):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 获取小说的信息
def get_novel_info(list1, name_list):
    for i, url in enumerate(list1):
        html = etree.HTML(get_text(url, headers))
        name = name_list[i]  # 书名
        title_url = html.xpath('//div[@id="list"]/dl/dd/a/@href')
        title_url = ['http://www.xbiquge.la' + i for i in title_url]  # 章节地址
        titlename_list = html.xpath('//div[@id="list"]/dl/dd/a/text()')  # 章节名字列表
        get_content(title_url, titlename_list, name)


# # 获取小说每章节的内容
def get_content(url_list, title_list, name):
    for i, url in enumerate(url_list):
        item = {}
        html = etree.HTML(get_text(url, headers))
        content_list = html.xpath('//div[@id="content"]/text()')
        content = ''.join(content_list)
        content=content+'\n'
        item['title'] = title_list[i]
        item['content'] = content.replace('\r\r', '\n').replace('\xa0', ' ')
        print(item)
        with open(name + '.txt', 'a+',encoding='utf-8') as file:
            file.write(item['title']+'\n')
            file.write(item['content'])


def main():
    base_url = 'http://www.xbiquge.la/xiaoshuodaquan/'
    html = etree.HTML(get_text(base_url, headers))
    novelurl_list = html.xpath('//div[@class="novellist"]/ul/li/a/@href')
    name_list = html.xpath('//div[@class="novellist"]/ul/li/a/text()')
    print(name_list)
    get_novel_info(novelurl_list, name_list)


if __name__ == '__main__':
    main()


