import requests,re
def start(company):

    headers={
            'authority':'www.qcc.com',
            'method': 'GET',
            # 'path': f'/search?key={company}',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'acw_tc=7a0e2b8515954846765241789e78d804e5d0040e63cb99094bed4b647c;'
            'cookie': f'UM_distinctid=172a0e936e536-0ed257d007e146-f7d1d38-13c680-172a0e936e642d; zg_did=%7B%22did%22%3A%20%22172a0e93710f3-09a19957512d21-f7d1d38-13c680-172a0e937121be%22%7D; _uab_collina=159183753841910492344504; QCCSESSID=vf2otfjr7ikglh0lbaf4e3uvm2; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1594947056,1595466696; hasShow=1; CNZZDATA1254842228=1279155518-1591832347-https%253A%252F%252Fsp0.baidu.com%252F%7C1595470804;  zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22info%22%3A%201594947055312%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%22e744443c27f6b9ad271ef883bca089a2%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=',
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
    url=f'https://www.qcc.com/search?key={company}'
    with open("cookies_bendi1.txt", "r") as f:
        cookies = f.readlines()[0][16:-2]
        cookie = str(cookies[2:-2]).replace('": "', '=').replace('", "', ';')
        headers['cookie'] = cookie
        con = requests.get(url, headers=headers, params=data).content.decode('utf-8').replace('\r', '').replace(
            '\t', '').replace('\n', '').replace(' ', '').replace("'", '').replace("{", '').replace("}", '')
        qyid = re.findall(f"内容类型:企业,内容名称:{company},内容链接:/firm/(.*?).html,内容位置:第1个", con)
        if qyid:
            qyid = qyid[0]
            return qyid
        else:
            print('cc')

        print(headers)

start('河北坤通建筑工程有限公司')
