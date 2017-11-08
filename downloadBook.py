# -*- coding = utf-8 -*-
from bs4 import BeautifulSoup
import requests, sys

index = input("请输入小说地址(仅限笔趣阁内的小说，例如：http://www.biqukan.com/0_790/):\n")


class downloader(object):
    def __init__(self, index):
        self.index = index
        self.head_url = self.getUrl(self.index)
        self.title = ""  # 小说的标题
        self.names = []  # 存放章节名字
        self.urls = []  # 存放章节链接
        self.num = []  # 章节总数

    def getUrl(self, long_url):
        x = self.index.split(".")
        x[-1] = x[-1][:3]
        url = ".".join(x)
        return url

    # 获取html内容
    def getHtml(self, url):
        res = requests.get(url)
        html = BeautifulSoup(res.text)
        return html

    # 获取下载链接、章节名、最新章节
    def get_download_url(self):
        html = self.getHtml(self.index)
        self.title = html.find('h2').string
        self.names = [a.string for a in (html.find_all('a'))][41:-11]  # 去除首尾不必要的内容
        self.urls = [a.get('href') for a in (html.find_all('a'))][41:-11]
        self.num = len(self.urls)

    # 获取章节内容
    def getText(self, url):
        url = self.head_url + url
        html = self.getHtml(url)
        texts = html.find_all('div', 'showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    # 写入文件
    def write(self, name, filename, text):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


c = downloader(index)
c.get_download_url()
# 自动取标题
title = "《" + c.title + "》"
print(title + '开始下载....\n')
for i in range(c.num):
    c.write(c.names[i], c.title + '.txt', c.getText(c.urls[i]))
    sys.stdout.write("  已下载:%.2f%%" % float((i / c.num) * 100) + '\r')  # 乘以100是为了更正确的显示
    sys.stdout.flush()
print(title + '下载完成')
