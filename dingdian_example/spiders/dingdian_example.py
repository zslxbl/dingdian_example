import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request  # 一个单独的request模块，需要跟进url的时候，需要用它
from dingdian_example.items import DingdianExampleItem  ##这是自定义的需要保存的字段


class MySpider(scrapy.Spider):
    name = 'dingdian_example'
    allowed_domains = ['23us.com']
    bash_url = 'http://www.23us.com/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
            # yield Request('http://www.23us.com/quanben/1

    def parse(self, response):
        # print(response.text)
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1, int(max_num) + 1):
            url = bashurl + '_' + str(num) + self.bashurl
            # print(url)
            yield Request(url, callback=self.get_name)
            '''
            yield Request,请求新的url，后面跟的是回调函数，你需要
            哪一个函数来处理这个返回值，就调用哪一个函数，
            返回值会以参数的形式传递给你所调用的函数
            '''

    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            '''
            这里使用循环的原因是find_all取出来的标签是以列表形式存在的，
            不然没办法继续使用find
            '''
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl, callback=self.get_chapterurl, meta={
                'name': novelname,
                'url': novelurl
            })

    def get_chapterurl(self, response):
        item = DingdianExampleItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['novelurl']
        category = BeautifulSoup(response.text, 'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[1].get_text()
        bash_url = BeautifulSoup(response.text, 'lxml').find('p', class_='btnlinks').find('a', class_='read')['href']
        item['category'] = category
        item['authon'] = author
        item['bash_url'] = bash_url

        return item



















