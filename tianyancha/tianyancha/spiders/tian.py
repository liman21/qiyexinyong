import scrapy,re,csv


# redis_cli = redis.Redis(host='127.0.0.1',port=6379)
redis_cli ='d'

class TianSpider(scrapy.Spider):
        name = 'search'
        # num = 0
        allowed_domains = ['www.tianyancha.com']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Host': 'www.tianyancha.com',
            'Referer': 'www.tianyancha.com',
            'Cookie': 'jsid=SEM-BAIDU-PZ0703-VIP-000001; TYCID=7cd9b660e11f11ea803fcb765b576429; ssuid=1424203815; bannerFlag=false; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1597733596; _ga=GA1.2.1809497357.1597733596; _gid=GA1.2.1161873128.1597733596; RTYCID=dff456a7426d402aae97c85df852c5a2; aliyungf_tc=AQAAAN4tzioY4gEARdMwkCcNgO3wEkI+; CLOUDID=9a200bc7-1866-4383-b27a-aca745d5150e; CT_TYCID=5da1d53f0069476e8badf601e7b79862; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1597733848; _gat_gtag_UA_123487620_1=1; cloud_token=4476d0f4f26b480dbadb8109918442d0; cloud_utm=d19274d0df03412cb4315c098f01dba4'
        }

        def start_requests(self):
            start_urls = 'https://www.tianyancha.com/company/4270923'
            yield scrapy.FormRequest(url=start_urls,headers=self.headers,callback=self.index_parse)
        def index_parse(self, response):
            # 主要人员
            zhuyaory_list=response.xpath('//*[@id="_container_staff"]/div/table/tbody/tr')
            # 股东信息
            gudong_list=response.xpath("//div[@id='_container_holder']/table[@class='table']/tbody/tr")
            # 对外投资
            touzi_list=response.xpath('//*[@id="_container_invest"]/div/table/tbody/tr')
            # 分支机构
            fenzhi_list=response.xpath('//*[@id="_container_branch"]/table/tbody/tr')
            # 开庭公告
            kaiting_list=response.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr')
            for ry in zhuyaory_list:
                # 主要人员名称
                ry_name=ry.xpath('./td[2]//td[2]/a/text()').extract()[0]
                # 职位
                zhiwei=ry.xpath('./td[3]//text()').extract()[0]
            for gudong in gudong_list:
                # 股东
                gu_name=gudong.xpath('./td[2]//text()').extract()[1]
                # 持股比例
                chigu=gudong.xpath('./td[3]//span/text()').extract()[0]
                # 认缴出资额
                chuzie=gudong.xpath('./td[4]//span/text()').extract()[0]
            for tz in touzi_list:
                # 被投资企业名称
                beitouzi_name=tz.xpath('./td[2]//a/text()').extract()[0]
                # 法定代表人
                daibiaoren=tz.xpath('./td[3]//div[1]//a/text()').extract()[0]
                # 成立日期
                chengli_date=tz.xpath('./td[4]/span/text()').extract()[0]
                # 投资数额
                touzi_value=tz.xpath('./td[5]/span/text()').extract()[0]
                # 投资比例
                touzi_proportion=tz.xpath('./td[6]/span/text()').extract()[0]
                # 经营状态
                jingying=tz.xpath('./td[7]/span/text()').extract()[0]
                # 关联产品
                guanlian_chanpin=tz.xpath('./td[8]//text()').extract()[0]
                # 关联机构
                guanlian_jigou=tz.xpath('./td[9]//text()').extract()[0]
                # 企业名称
                qy_name = tz.xpath('./td[2]//text()').extract()[1]
                # 负责人
                fuzeren = tz.xpath('./td[3]//td[2]//text()').extract()[0]
            for fenzhi in fenzhi_list:
                # 分支机构 企业名称
                fz_qy = fenzhi.xpath('.//td[2]//a/text()').extract()[0]
                 # 分支机构 负责人
                fz_fzr = fenzhi.xpath('.//td[3]//td[2]/a/text()').extract()[0]
                # 分支机构 成立日期
                fz_clrq = fenzhi.xpath('.//td[4]/span/text()').extract()[0]
                # 分支机构 经营状态
                fz_jyzt = fenzhi.xpath('.//td[5]/span/text()').extract()[0]
                z_qy = fenzhi.xpath('.//td[2]//a/text()').extract()[0]
                # 分支机构 负责人
                fz_fzr = fenzhi.xpath('.//td[3]//td[2]/a/text()').extract()[0]

            for kaiting in kaiting_list:
                # 开庭公告 开庭日期
                kt_rq = kaiting.xpath('./td[2]/text()').extract()[0]
                # 案号
                kt_ah = kaiting.xpath('./td[3]/span/text()').extract()[0]
                # 案由
                kt_rq = kaiting.xpath('./td[4]/span/text()').extract()[0]
                # 公诉人/原告/上诉人/申请人
                kt_gsr = kaiting.xpath('./td[5]//text()').extract()[0]
                # 被告人/被告/被上诉人/被申请人
                kt_gsr = kaiting.xpath('./td[6]//text()').extract()[0]
                # 详情
                kt_gsr = kaiting.xpath('./td[7]//@data-businessid').extract()[0]
                con=response.text

                print('dd')

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute('scrapy crawl search'.split())

