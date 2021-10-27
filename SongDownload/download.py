import os
import re

import requests
from scrapy.selector import Selector


class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url = 'http://music.163.com/'
        # session实例化对象
        self.session = requests.Session()
        self.session.headers = self.headers

    def get_resp(self, url):
        """发送url请求，返回响应内容"""
        # 发送请求，获取响应
        resp = self.session.get(url)  # 直接用session进入网页
        # 返回响应内容
        return resp.content

    def get_songurls(self, playlist):
        '''进入所选歌单页面，得出歌单里每首歌各自的ID 形式就是“song?id=64006"'''
        url = self.main_url + 'playlist?id=%d' % playlist
        # 获取内容
        content = self.get_resp(url)
        # Scrapy选择器是Selector通过传递文本或TextResponse对象构造的类的实例。
        # 根据输入类型自动选择最佳的解析规则（XML与HTML）
        sel = Selector(text=content)  # 用scrapy的Selector
        songurls = sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls  # 所有歌曲组成的list

    def get_songinfo(self, songurl):
        '''根据songid进入每首歌信息的网址，得到歌曲的信息'''
        url = self.main_url + songurl
        # 发送请求，获取响应
        resp = self.session.get(url)
        # 解析响应内容
        sel = Selector(text=resp.text)
        # 获取song_id
        song_id = url.split('=')[1]
        # 获取song_name
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        # 获取singer
        singer = '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        # 组装songname
        songname = singer + '-' + song_name
        # 返回
        return str(song_id), songname

    def download_song(self, song_url, songname, dir_path):
        '''根据歌曲url，下载mp3文件'''
        # 文件名中不能含有特殊字符
        # songname = re.sub(r"[/]", ",", songname)
        songname = re.sub(r"[?!@#$%^&*()/]", "", songname)
        # os.sep相当于 “//”
        path = dir_path + os.sep + songname + '.mp3'  # 文件路径
        # 获取内容
        content = self.get_resp(song_url)
        # 保存到本地
        with open(path, "wb") as f:
            f.write(content)
        print(songname, "下载完毕！")

    def work(self, playlist):
        # 输入歌单编号，得到歌单所有歌曲的url
        songurls = self.get_songurls(playlist)
        # 指定歌曲存放位置
        dir_path = r'./music'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        # 遍历下载歌单中所有歌曲
        for songurl in songurls:
            # 根据歌曲url得出ID、歌名
            song_id, songname = self.get_songinfo(songurl)
            # 拼接下载歌曲的url
            song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % song_id
            # 下载歌曲
            self.download_song(song_url, songname, dir_path)


if __name__ == '__main__':
    d = wangyiyun()
    d.work(5309137927)  # 歌单id
