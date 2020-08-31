import requests,re
urls='https://www.dianping.com/search/keyword/24/0_%E4%B8%BD%E4%BA%BA'
header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'fspop=test; cy=24; cye=shijiazhuang; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=174056985ffc8-02b663a2ca343d-3323767-13c680-174056985ffc8; _lxsdk=174056985ffc8-02b663a2ca343d-3323767-13c680-174056985ffc8; _hc.v=bc3ce3fc-a29b-e798-0d06-fab3c33c4257.1597818637; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597818637; s_ViewType=10; _lxsdk_s=17405698604-8e3-c9f-ac9%7C%7C39; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1597818687',
    'Host': 'www.dianping.com',
    'Referer': 'https://www.dianping.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
contt=requests.get(urls,headers=header).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
idss=re.findall('data-fav-referid="(\w+)" data-fav-favortype="1" data-name="(.*?)"><i></i><span>',contt)
for cc in idss:
    id=cc[0]
    shop=cc[1]
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'cy=24; cityid=24; cye=shijiazhuang; fspop=test; cy=24; cye=shijiazhuang; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=174056985ffc8-02b663a2ca343d-3323767-13c680-174056985ffc8; _lxsdk=174056985ffc8-02b663a2ca343d-3323767-13c680-174056985ffc8; _hc.v=bc3ce3fc-a29b-e798-0d06-fab3c33c4257.1597818637; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597818637; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1597818667; _lxsdk_s=17405698604-8e3-c9f-ac9%7C%7C38',
        'Host': 'www.dianping.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    url=f'http://www.dianping.com/shop/{id}'
    con=requests.get(url,headers=headers).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
    content=re.findall('Description" content="(.*)"/><meta name="location" ',con)
    if content:
        content=content[0].split('电话：')
        adress=content[0].replace('，','')
        tell=content[1].split('营业时间')[0]('，','')
        print('ff')