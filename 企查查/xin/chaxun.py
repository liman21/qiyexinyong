import random
import requests
import os
# from usagen import USER_AGENTS
# from connect_redis import redis_save
# from mongo import save_name
from 企查查.xin1.xinxi_data import *
import datetime

# def get_ip():
#     while True:
#         try:
#             cf = configparser.ConfigParser()
#             cf.read("./config.ini")
#             yun_ip = cf.get("Redis", "yun_ip")
#             keyword = redis_save.rpop(yun_ip)
#             redis_save.lpush(yun_ip, keyword)
#             ips=keyword.decode("utf-8")
#             proxyusernm = "lxk950516"  # 代理帐号
#             proxypasswd = "lxk417215"  # 代理密码
#             ip = proxyusernm + ":" + proxypasswd + "@" + ips
#             proxies = {'http': "http://" + ip,
#                        'https': "https://" + ip}
#             print(proxies)
#             return  proxies
#         except Exception as e:
#             print(e)
USER_AGENTS = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

def get_session():
    now = int(time.time())
    ts = int(datetime.datetime.now().timestamp() * 1000)
    tt=f'"sid": {ts},"updated": {ts},'
    headers={
        'authority':'www.qcc.com',
        'method': 'GET',
        # 'path': f'/search?key={company}',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'acw_tc=7a0e2b8515954846765241789e78d804e5d0040e63cb99094bed4b647c;'
        'cookie': f'UM_distinctid=172a0e936e536-0ed257d007e146-f7d1d38-13c680-172a0e936e642d; zg_did=%7B%22did%22%3A%20%22172a0e93710f3-09a19957512d21-f7d1d38-13c680-172a0e937121be%22%7D; _uab_collina=159183753841910492344504; QCCSESSID=vf2otfjr7ikglh0lbaf4e3uvm2; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1594947056,1595466696; hasShow=1; CNZZDATA1254842228=1279155518-1591832347-https%253A%252F%252Fsp0.baidu.com%252F%7C1595470804;  zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B{tt}%22info%22%3A%201594947055312%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%22e744443c27f6b9ad271ef883bca089a2%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb={now}',
        # 'referer': f'https://www.qcc.com/search?key={company}',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    os.system("python huakuai.py")
    with open("cookies_bendi1.txt", "r") as f:
        cookies = f.readlines()[0][16:-2]
        cookie = str(cookies[2:-2]).replace('": "', '=').replace('", "', ';')
        headers['cookie'] = cookie
        return headers

    #
    # con=driver.page_source


def get_url(company,headers):
    while True:
        data = {
            'key': f'{company}'
        }
        url1 = f'https://www.qcc.com/search?key={company}'
        con1 = requests.get(url1, headers=headers, params=data).content.decode('utf-8').replace('\r', '').replace(
            '\t', '').replace('\n', '').replace(' ', '').replace("'", '').replace("{", '').replace("}", '')
        qyid = re.findall(f"内容类型:企业,内容名称:{company},内容链接:/firm/(.*?).html,内容位置:第1个", con1)
        if qyid:
            qyid = qyid[0]
            keyword = f"{company}###{qyid}"
            if keyword:
                print("开始请求数据")
                keyword_decode = keyword
                key = keyword_decode.split("###")
                print("the key is------------ ", keyword_decode)
                url = "https://www.qcc.com/firm_{}.html".format(key[1])
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
                              'user-agent': random.choice(USER_AGENTS),
                }
                o=1
                if o==1:
                # try:
                    # res = requests.get(url, headers=headers,proxies=get_ip(),timeout=5)
                    res = requests.get(url, headers=headers,timeout=5)
            #         print(res.text)
            #         content=res.content.decode('utf-8').replace('\r','').replace('\t','').replace('\n','')
                    if res.status_code == 200:
                        return 1
            #             if 'location' in res.text[0:30]:
            #                 raise Exception("*********************ip不行")
            #             else:
            #                 html = etree.HTML(res.text)
            #                 # 开始获取信息
            #                 orgName1 = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1/text()')
            #                 if orgName1 == []:
            #                     orgName1 = html.xpath('//div[@class="content"]/div/h1/text()')
            #                 orgName = orgName1[0]
            #                 # try: # def get_data(html,qcc_id,orgName)
            #                 dic = get_data(html, key[1],orgName,content)
            #                 # except Exception:
            #                 #     dic = get_g(html, key[1],orgName)
            #                 print(dic)
            #                 # try:
            #                 #     save_name.new(dic)
            #                 # except Exception as e:
            #                 #     with open("xinxi_chongfu.txt", "a", encoding="utf-8")as f:
            #                 #         f.write(keyword_decode + "\n")
            #                 # name_id = keyword_decode + "###" + orgName
            #                 # with open("ok_company.txt", "a", encoding="utf-8")as f:
            #                 #     f.write(name_id + "\n")
            #     except Exception as e:
            #         print(e)
                #     redis_save.lpush(company_url, keyword)
                    # redis_save.lpush(qcc_cookies, cookie)
                    # print("------------------没有获取到该 url， 请放入队列重新查看！-------------------")
            # else:
            #     print("跑完了！！！")
            #     break

        else:
            print('ff')
def start():
    i=0
    headers = get_session()
    while True:
        com=input('请输入要查询公司')
        cc=get_url(com,headers)
        if cc!=None:
            i+=1
            print(f'测试了{i}次')
        else:
            print('ff')
            return start()

if __name__ == '__main__':
    start()

