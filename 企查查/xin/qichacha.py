import random
import requests
import os,json
# from usagen import USER_AGENTS
# from connect_redis import redis_save
from dao import Mysql

from 企查查.xin1.xinxi_data import *
import datetime

def ipmax():
    try:
        url = 'http://api.ip.data5u.com/dynamic/get.html?order=37f0fd23d9166d931a5e390f55813332&json=1&random=1&sep=3'
        a = requests.get(url, timeout=5).text
        if not a.find('data') == -1:
            b = json.loads(a)['data']
            c = str(b[0]["ip"]) + ":" + str(b[0]["port"])
            ip = {"http": "http://" + c, "https": "https://" + c}
            return ip
        elif a.find('请控制好请求频率') != -1:
            time.sleep(1)
            return ipmax()
        else:
            return ipmax()
    except Exception as e:
        print(e)
        return ipmax()
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

def get_id(company):
    url=f'https://www.qcc.com/search?key={company}'
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
        'cookie': f'Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1596013637;acw_tc=6f7e789715960136364107111e658a606113c5b7d4e0de41cce42be832;UM_distinctid=17399d36cce204-07ef35a7b6f16c-b363e65-13c680-17399d36ccf38f;QCCSESSID=6odkg7m8oc4c7gmqapbplludk3;_uab_collina=159601363669250647322886;zg_did=%7B%22did%22%3A%20%2217399d36c1162-0187c178a0c29b-b363e65-13c680-17399d36c1265b%22%7D;Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1596013637;CNZZDATA1254842228=307711671-1596010379-%7C1596010379;zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201596013636631%2C%22updated%22%3A%201596013637203%2C%22info%22%3A%201596013636636%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D',
        # 'referer': f'https://www.qcc.com/search?key={company}',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    data={
        'key':f'{company}'
    }
    f=Mysql.select_qycookie()
    cookies = f[1][16:-2]
    cookie = str(cookies[2:-2]).replace('": "', '=').replace('", "', ';')
    headers['cookie'] = cookie
    con=requests.get(url,headers=headers,params=data,proxies=ipmax()).content.decode('utf-8').replace('\r','').replace('\t','').replace('\n','').replace(' ','').replace("'",'')
    if 'location' in con[0:30] or 'varexpiredate' in con[:-50]:
        Mysql.delete_qycookie(uid=f[0])
        return get_id(company)
    else:
        qyid=re.findall(f"内容类型:企业,内容名称:{company},内容链接:/firm/(.*?).html,内容位置:第1个",con)
        if qyid:
            qyid=qyid[0]
            return qyid
        else:
            print('ff')
            # os.system("python huakuai.py")
            # with open("cookies_bendi1.txt", "r") as f:
            #     cookies = f.readlines()[0][16:-2]
            #     cookie = str(cookies[2:-2]).replace('": "', '=').replace('", "', ';')
            #     headers['cookie'] = cookie
            #     con = requests.get(url, headers=headers, params=data,proxies=ipmax()).content.decode('utf-8').replace('\r', '').replace(
            #         '\t', '').replace('\n', '').replace(' ', '').replace("'", '').replace("{", '').replace("}", '')
            #     qyid = re.findall(f"内容类型:企业,内容名称:{company},内容链接:/firm/(.*?).html,内容位置:第1个", con)
            #     if qyid:
            #         qyid = qyid[0]
            #         return qyid
            #     else:
            #         print('cc')

    #
    # con=driver.page_source


def get_url(company):
    while True:
        # print("启动线程 %d" % num)
        # cf = configparser.ConfigParser()
        # cf.read("./config.ini")
        # company_url = cf.get("Redis" ,"company_url")
        # # 获取cookie
        # qcc_cookies = cf.get("Redis", "company_cookies")
        # cookie = redis_save.rpop(qcc_cookies)
        # ok_cookies = cookie.decode("utf-8")
        # company = input('输入要查询的公司名：')
        qyid=get_id(company)
        if qyid!=None:
            # keyword = redis_save.rpop(company_url)
            keyword = f"{company}###{qyid}"
            if keyword:
                print("开始请求数据")
                # keyword_decode = keyword.decode("utf-8")
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
                    res = requests.get(url, headers=headers,proxies=ipmax(),timeout=5)
                    # res = requests.get(url, headers=headers,timeout=5)
            #         print(res.text)
                    content=res.content.decode('utf-8').replace('\r','').replace('\t','').replace('\n','')
                    if res.status_code == 200:
                        print(content)
                        if 'location' in res.text[0:30]:
                            print("*********************ip不行")
                            return get_url(company)
                        else:
                            html = etree.HTML(res.text)
                            # 开始获取信息
                            orgName1 = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1/text()')
                            orgName2 = html.xpath('//div[@class="content"]/div/h1/text()')
                            if len(orgName1)>0:
                                orgName = orgName1[0]
                                dic = get_data(html, key[1], orgName, content)
                            elif len(orgName2)>0:
                                orgName = orgName2[0]
                                dic = get_data(html, key[1], orgName, content)
                            else:
                                dic=''
                            print(dic)
                            return 1

        else:
            print('ff')


if __name__ == '__main__':
    # thread_list = []
    # for i in range(1):
    #     th = Thread(target=get_url, args=(i,))
    #     th.start()
    i=0
    while True:
        cc=get_url('河北坤通建筑工程有限公司')
        if cc!=None:
            i+=1
            print(f'测试了{i}次')
        else:
            print('ff')
