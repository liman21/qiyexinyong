import random
import requests
from lxml import etree
from 企查查.xin1.xinxi_data import *
import datetime
import os,json

def get_url():
    while True:
        print("开始请求数据")
        # qcc_idword_decode = qcc_idword.decode("utf-8")
        # qcc_id='25F4AXI'  # 河北坤通
        qcc_id='426LNEG'  # 平煤神马
        url = f"https://www.qcc.com/firm/{qcc_id}.html"
        # url = "https://m.qcc.com/firm_9cce0780ab7644008b73bc2120479d31.shtml"
        headers = {
                      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                      'accept-encoding': 'gzip, deflate, br',
                      'accept-language': 'zh-CN,zh;q=0.9',
                      'cache-control': 'max-age=0',
                      # 'cookie': ok_cookies,
                      'referer': 'https://www.qcc.com/',
                      'sec-fetch-mode': 'navigate',
                      'sec-fetch-site': 'same-origin',
                      'sec-fetch-user': '?1',
                      'upgrade-insecure-requests': '1',
                      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }
        o=1
        if o==1:
        # try:
        #     res = requests.get(url, headers=headers,proxies=ipmax(),timeout=5)
            res = requests.get(url, headers=headers,timeout=5)
    #         print(res.text)
            content=res.content.decode('utf-8').replace('\r','').replace('\t','').replace('\n','')

            if res.status_code == 200:
                print(content)
                if 'location' in res.text[0:30]:
                    print("*********************ip不行")
                else:
                    html = etree.HTML(res.text)
                    # 开始获取信息
                    intelligencetype1 = re.findall(
                        '<tr> <td class="tx">(\d+)</td> <td width="150" class="text-left">(.*?)</td> <td width="135" class="text-left"> <a onclick="(.*?)\)">(.*?)</a> </td> <td>(.*?)</td> <td width="104" class="text-center">(.*?)</td> <td width="104" class="text-center">(.*?)</td> <td width="104" class="text-left">(.*?)</td> </tr>',
                        content)
                    if len(intelligencetype1) > 0:
                        intelligencetype = []
                        for intelligencetypes in intelligencetype1:
                            zzlx = intelligencetypes[1].strip()
                            zsh = intelligencetypes[3]
                            zzfw = intelligencetypes[4]
                            zzfw1 = intelligencetypes[4].split(',')
                            fzrq = intelligencetypes[5]
                            zsyxq = intelligencetypes[6]
                            fzjg = intelligencetypes[7]
                            igtype = [zzlx, zsh, zzfw, fzrq, zsyxq, fzjg]
                            intelligencetype.append(igtype)
                            if len(zzfw1) > 1:
                                print('含有多个资质名称')
                                # for i in range(len(zzfw1)):
                                #     zzmc = zzfw1[i]
                                #     select = Mysql.select_qyzz(qyid=qcc_id, zzmc=zzmc)
                                #     if len(select) > 0:
                                #         print(f'数据已存在[{zsh}]')
                                #     else:
                                #         Mysql.insert_qyzz(qyid=qcc_id, zzlx=zzlx, zsh=zsh, zzmc=zzmc, fzrq=fzrq,
                                #                           zsyxq=zsyxq, fzjg=fzjg,
                                #                           zzfw=zzfw)
                            else:
                                print('单个资质证书')
                                # select = Mysql.select_qyzz(qyid=qcc_id, zzmc=zzfw)
                                # if len(select) > 0:
                                #     print(f'数据已存在[{zsh}]')
                                # else:
                                #     Mysql.insert_qyzz(qyid=qcc_id, zzlx=zzlx, zsh=zsh, zzmc=zzfw, fzrq=fzrq,
                                #                       zsyxq=zsyxq, fzjg=fzjg,
                                #                       zzfw=zzfw)
                    else:
                        print('该公司无资质证书内容')


            html1 = etree.HTML(content)
        #   经营状况
            jiying_zk = html1.xpath(
                "//div[@class='company-nav-tab                                                                             '][2]/a[@class='company-nav-head']/@href")[
                0]
            jyzk_url = 'https://www.qcc.com/' + jiying_zk
            header = {
                # ':authority: www.qcc.com'
                # :method: GET
                # :path: /crun/d9dd3459c80cf338f83002e68c3fb99b
                # :scheme: https
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'UM_distinctid=1740045de949e4-07bc1afbec259-3323765-13c680-1740045de958dd; zg_did=%7B%22did%22%3A%20%221740045df7f15a-00733504578a32-3323765-13c680-1740045df80198%22%7D; _uab_collina=159773241341246389995574; hasShow=1; QCCSESSID=bc5t9f2074t5ar5fbq1cdpud45; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1597737549,1597806877,1597825565,1597826442; acw_tc=6a75d59e15978274596241922ecee30c8d16398f48b0225c28e4fb5000; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201597828556041%2C%22updated%22%3A%201597828556421%2C%22info%22%3A%201597732413328%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; CNZZDATA1254842228=420593471-1597730584-https%253A%252F%252Fwww.baidu.com%252F%7C1597827097; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1597828557',
                # 'referer': 'https://www.qcc.com//crun/d9dd3459c80cf338f83002e68c3fb99b',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
            }
            res1 = requests.get(jyzk_url, headers=header, timeout=5)
            if res1.status_code == 200:
                ress=res1.content.decode('utf-8')
                html2 = etree.HTML(ress)
                zhaotb_list=html2.xpath('//*[@id="tenderlist"]/table/tbody/tr')
                for i in range(2,len(zhaotb_list)+1):
                    zhao_xpath=f'//*[@id="tenderlist"]/table/tbody/tr[{i}]'
                    xiangmu=html2.xpath(zhao_xpath+'/td[2]/a/text()')[0]
                    publictime=html2.xpath(zhao_xpath+'/td[3]/text()')[0].strip()
                    pro=html2.xpath(zhao_xpath+'/td[4]/text()')[0].strip()
                    leixing=html2.xpath(zhao_xpath+'/td[5]/span/text()')[0].strip()
                    print('行政许可：',xiangmu,publictime,pro,leixing)
                    print('fff')
            jiying_fx = html1.xpath(
                "//div[@class='company-nav-tab                                                                             '][3]/a[@class='company-nav-head']/@href")[
                0]
            jyfx_url = 'https://www.qcc.com/' + jiying_fx
            header1 = {
                # ':authority: www.qcc.com'
                # :method: GET
                # :path: /crun/d9dd3459c80cf338f83002e68c3fb99b
                # :scheme: https
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'UM_distinctid=1740045de949e4-07bc1afbec259-3323765-13c680-1740045de958dd; zg_did=%7B%22did%22%3A%20%221740045df7f15a-00733504578a32-3323765-13c680-1740045df80198%22%7D; _uab_collina=159773241341246389995574; hasShow=1; QCCSESSID=bc5t9f2074t5ar5fbq1cdpud45; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1597737549,1597806877,1597825565,1597826442; acw_tc=6a75d59e15978274596241922ecee30c8d16398f48b0225c28e4fb5000; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201597828556041%2C%22updated%22%3A%201597828556421%2C%22info%22%3A%201597732413328%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; CNZZDATA1254842228=420593471-1597730584-https%253A%252F%252Fwww.baidu.com%252F%7C1597827097; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1597828557',
                # 'referer': 'https://www.qcc.com//crun/d9dd3459c80cf338f83002e68c3fb99b',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
            }
            res2= requests.get(jyfx_url, headers=header1, timeout=5)
            if res2.status_code == 200:
                resss = res2.content.decode('utf-8')
                html22 = etree.HTML(resss)
                # 欠税公告
                qs_list=html22.xpath('//*[@id="owenoticelist"]/table/tbody/tr')
                for i in range(2,len(qs_list)+1):
                    qs_xpath=f'//*[@id="owenoticelist"]/table/tbody/tr[{i}]'
                    # 欠税税种
                    qssz=html22.xpath(qs_xpath+'/td[2]/a/text()')[0].script()
                    # 欠税余额
                    qsye=html22.xpath(qs_xpath+'/td[3]/text()')[0].script()
                    # 当前新发生的欠税金额
                    new_qsye=html22.xpath(qs_xpath+'/td[4]/text()')[0].script()
                    # 发布单位
                    fbdw=html22.xpath(qs_xpath+'/td[5]/text()')[0].script()
                    # 发布日期
                    fbrq=html22.xpath(qs_xpath+'/td[6]/text()')[0].script()
                    print('欠税公告:',qssz,qsye,new_qsye,fbdw,fbrq)
                    print('ff')




                    
get_url()