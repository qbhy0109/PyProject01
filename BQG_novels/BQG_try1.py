import requests
from lxml import etree


url = 'https://www.xbiquge.la'


# 获取网页文本
def get_html(url):
    req = requests.get(url=url)
    req.encoding = 'utf-8'
    return req.text


def main():
    target_url = 'https://www.xbiquge.la/xiuzhenxiaoshuo'
    html = etree.HTML(get_html(target_url))
    # novel_name = input('请输入小说名字：')
    novel = html.xpath('//span[@class="s2"]/a[contains(text(),"遮天")]')[0]
    print(novel.text,novel.attrib['href'])
    get_novel(novel.attrib['href'], novel.text)


def get_novel(novel_url, novel_name):
    html = etree.HTML(get_html(novel_url))
    chapters = html.xpath('//div[@id="list"]/dl/dd/a')
    for i, chap in enumerate(chapters):
        chapter_url = url + chap.attrib['href']
        chapter_name = chap.text
        print(chapter_name)
        chapter_html = etree.HTML(get_html(chapter_url))
        chapter_content = chapter_html.xpath('//div[@id="content"]/text()')
        chapter_content = ''.join(chapter_content)
        chapter_content = chapter_content.replace('\r\r', '\n').replace('\xa0', '  ')
        with open('《'+novel_name + '》' + '.txt', 'a+', encoding='utf-8') as file:
            file.write(chapter_name+'\n\n')
            file.write(chapter_content+'\n\n')


if __name__ == '__main__':
    main()





