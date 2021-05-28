import scrapy
import pandas as pd
import time


class QuotesSpider(scrapy.Spider):
    name = "keyFinder"
    df = None
    totalNumber = 0     # 总数量
    curNumber = 0       # 已处理数量
    _dict = {}
    startTime = 0

    def start_requests(self):
        self.startTime = time.time()
        self.df = pd.read_csv('test.csv')
        self.totalNumber = len(self.df['URL'])
        for url in self.df['URL']:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errorSolve)
    

    def closed(self, reason):
        self.df['info'] = ''        # Add a new column called 'info'
        for i in range(self.totalNumber):
            self.df['info'][i] = self._dict[self.df['URL'][i]]
        self.df.to_csv("output.csv",index=False,sep=',')
        timecost = time.strftime("%H:%M:%S", time.gmtime(round(time.time() - self.startTime)))
        self.log('Total time cost: ' + timecost)
        self.log('Save file to output.csv')


    def errorSolve(self, failure):
        self.log(failure)
        self.curNumber += 1
        self.log('********** Error ' + str(self.curNumber) + '/' + str(self.totalNumber) + ' ********** ')



    def parse(self, response):
        code_list = response.xpath('//td//span/text()').extract()
        for code in code_list:
            if code == 'cy':
                self._dict[response.url] = 'Cypress'
                self.curNumber += 1
                self.log('********** Cypress ' + str(self.curNumber) + '/' + str(self.totalNumber) + ' ********** ')
                return
        self._dict[response.url] = 'Other'
        self.curNumber += 1
        self.log('********** Other ' + str(self.curNumber) + '/' + str(self.totalNumber) + ' ********** ')
