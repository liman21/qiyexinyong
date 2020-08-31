# -*- coding: utf-8 -*-
import time, uuid, requests, json
from dao import Mysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup
# todo  湖北  公共资源中心  |住建局
def hubei(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,
                                  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        url='http://220.160.52.164:96/ConstructionInfoPublish/Pages/CompanyQuery.aspx?systemID=31'

        urls = {
            '39': '建筑业|1863',
            '31': '省外建筑业|555',
            '9': '招标代理|149',
            '42': '省外招标代理|25',
            '18': '一体化|18',
        }

        driver.get(url)
        for value, zzlxx in zip(urls.keys(), urls.values()):
            zzlx=zzlxx.split('|')[0]
            pages=int(zzlxx.split('|')[1])
            s1 = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder_ddlBussinessSystem'))  # 实例化Select
            s1.select_by_value(value)  #
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//table[@id='ctl00_ContentPlaceHolder_gvDemandCompany']/tbody/tr/td[1]/a"

            length = len(html_2.xpath(xpath)) + 2
            po = 0
            cc=10
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(2, length):
                    lengt = len(html_1.xpath(xpath))+1
                    xpath1 = xpath.replace('tr/td[', f'tr[{i}]/td[')

                    qyurl = 'http://220.160.52.164:96/ConstructionInfoPublish/Pages/'+html_1.xpath(f"{xpath1}/@href")[0].strip()
                    qyname = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t','').replace(
                        '\r', '').replace('(', '）').replace(')','）')
                    shxydm = html_1.xpath(f"{xpath1.replace('[1]/a','[6]')}/text()")[0].strip().replace('\n', '')

                    select = Mysql.select_fj(qyname=qyname,qyurl=qyurl)  # 查询标题是否存在

                    if select == None:
                        Mysql.insert_fj(qyname=qyname, shxydm=shxydm, qyurl=qyurl, zzlx=zzlx)

                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                if  page>pages-5:
                                    driver.find_element_by_xpath(f"//div[@id='ctl00_ContentPlaceHolder_pGrid']/table/tbody/tr/td[{cc}]/a").click()
                                    cc+=1
                                else:
                                    driver.find_element_by_xpath(f"//a[@id='ctl00_ContentPlaceHolder_pGrid_nextpagebtn']").click()

                        break
    except Exception as e:
        print('湖北\t', e)
        driver.close()
        return hubei(name)
hubei('福建')