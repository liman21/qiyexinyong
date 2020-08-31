import requests
from lxml import etree
from dao import Mysql
import time,re,json,datetime
from selenium import webdriver

def tianyancha(url):
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Cookie": "aliyungf_tc=AQAAAL9zfjMqLAQAGpXaG0rH+SQSMyir; csrfToken=D4W5eHOZUdVKKtVN8B5RcWil; jsid=SEM-BAIDU-PZ2003-VI-000001; TYCID=ee9c15b0727811eabdfbb3a9464b1d4e; undefined=ee9c15b0727811eabdfbb3a9464b1d4e; ssuid=7522613240; bannerFlag=false; _ga=GA1.2.2024087523.1585567433; _gid=GA1.2.1441861791.1585567433; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1585567432,1585568902; refresh_page=0; RTYCID=06e1215159ed40e9b936441fe8b79c12; token=9b83740966314eef9746e9fee609fd9a; _utm=8c3b6195c8d347ccab2335d8abd7a664; CT_TYCID=25b749040e3a45c98de53deb2d0d8104; cloud_token=9d4a9eb888e64a1bb4da17049cf08014; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1585571475; _gat_gtag_UA_123487620_1=1",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
    }

    item_list = {} # 存储队列

    response = requests.get(url, headers=headers).text  # 起始URL
    fen1 = etree.HTML(response)
    urls = fen1.xpath("//div[@class='search-item sv-search-company'][1]//div[@class='header']/a/@href")[0]

    time.sleep(1)
    response_content = requests.get(urls, headers=headers).text
    datalist = etree.HTML(response_content)

    item_list['注册资本'] = datalist.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div/text()')[0]
    item_list['公司类型'] = datalist.xpath("//table[@class='table -striped-col -border-top-none -breakall']/tbody/tr[5]/td[2]/text()")[0]
    item_list['营业期限'] = datalist.xpath("//table[@class='table -striped-col -border-top-none -breakall']/tbody/tr[7]/td[2]/span/text()")[0]


    # 企业资质详情
    xpath1='//*[@id="_container_constructQualification"]/div/table/tbody/tr/td[8]/span/@onclick'
    zz_urls= datalist.xpath(xpath1)

    for zz in range(1,len(zz_urls)+1):
        tt=datalist.xpath(xpath1.replace('tr/td[8]',f'tr[{zz}]/td[8]'))
        if tt:
            id=tt[0].replace('openConstructQualificationDetail','')[2:-2]
            ts = int(datetime.datetime.now().timestamp() * 1000)
            xq_url=f'https://capi.tianyancha.com/cloud-newdim/construct/getQualificationDetail.json?businessId={id}&_={ts}'
            cccc=requests.get(url).content.decode('utf-8')
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_experimental_option('w3c', False)
            chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
            chromeOptions.add_argument('--headless')  # 隐藏浏览器
            driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            driver.maximize_window()
            driver.get(xq_url)
            cc=driver.page_source
            con=re.findall('pre-wrap;">(.*?)</pre></body></html>',cc)

            if con:
                cont=json.loads(con[0])['data']['qualification']
                intelligencetype = []
                zzlx = cont['type']
                zsh = cont['certificateNum']
                zzfw = cont['qualificationName']
                zzfw1 = zzfw.split(',')
                fzrq = cont['issuingCertificateTime']
                zsyxq = cont['effectiveTime']
                fzjg = cont['organ']
                igtype = [zzlx, zsh, zzfw, fzrq, zsyxq, fzjg]
                intelligencetype.append(igtype)
                # if len(zzfw1) > 1:
                #     print('含有多个资质名称')
                #     for i in range(len(zzfw1)):
                #         zzmc = zzfw1[i]
                #         select = Mysql.select_qyzz(qyid=id, zzmc=zzmc)
                #         if len(select) > 0:
                #             print(f'数据已存在[{zsh}]')
                #         else:
                #             Mysql.insert_qyzz(qyid=id, zzlx=zzlx, zsh=zsh, zzmc=zzmc, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg, zzfw=zzfw)
                # else:
                #     select = Mysql.select_qyzz(qyid=id, zzmc=zzfw)
                #     if len(select) > 0:
                #         print(f'数据已存在[{zsh}]')
                #     else:
                #         Mysql.insert_qyzz(qyid=id, zzlx=zzlx, zsh=zsh, zzmc=zzfw, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg, zzfw=zzfw)
                # print('fff')

if __name__ == '__main__':

        company="河北坤通建筑工程有限公司"
        url = f"https://www.tianyancha.com/search/p1?key={company}" # 分页
        vv=tianyancha(url)

