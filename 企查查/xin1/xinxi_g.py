import time, hashlib, re
from lxml import etree


def get_g(html,qcc_id,orgName):
    # 开始获取信息 //*[@id="company-top"]/div[2]/div[2]/div[1]/h1

    taskId = hashlib.md5(orgName.encode(encoding='UTF-8')).hexdigest()
    update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))


    # 第二部分 登记信息
    orgLogo1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/div/div/div[1]/img')
    if orgLogo1:
        orgLogo = orgLogo1[0].get("src")
    else:
        orgLogo = ""

    # 法人  //*[@id="Cominfo"]/table/tbody/tr[1]/td[2]/div/div/div[2]/a[1]/h2
    corporation1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/div/div/div[2]/a[1]/h2/text()')
    corporation=corporation1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()


    # 法人连接
    legalLink1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/div/div/div[2]/a[1]')
    print(legalLink1[0].get("href"))
    if legalLink1:
        legalLink = "https://www.qcc.com" + legalLink1[0].get("href")
    else:
        legalLink = ""

    # 关联公司
    legalCompanyNum1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/div/div/div[2]/a[2]')
    if legalCompanyNum1:
        legalCompanyNum2 = legalCompanyNum1[0].text.replace("\n", "").replace("\r", "").replace("\t", "").strip()
        legalCompanyNum = re.findall("关联(.*?)家企业", legalCompanyNum2)[0]
    else:
        legalCompanyNum = ""

    # 经营状态

    enterpriseStatus1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[4]/text()')
    if enterpriseStatus1 == []:
        enterpriseStatus1 = html.xpath('//section[@id="Cominfo"]/table[@class="ntable"]/tbody/tr[1]/td[4]/text()')
    enterpriseStatus=enterpriseStatus1[0].replace("\n", "").replace("\r","").replace("\t", "").strip()
    if enterpriseStatus == "-":
        enterpriseStatus = ""


    # 举办单位

    sponsor1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[6]/text()')
    sponsor=sponsor1[0].replace("\n", "").replace("\r","").replace( "\t", "").strip()
    if sponsor == "-":
        sponsor = ''

    # 统一社会信用代码
    creditCode1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[2]/text()')
    creditCode=creditCode1[0].strip().replace("\n", "").replace("\r", "").replace("\t", "")
    if creditCode == "-":
        creditCode = ""


    # 开办资金
    start_money1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[4]/text()')
    start_money=start_money1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if start_money == "-":
        start_money = ""

    # 经费来源
    funding1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[6]/text()')
    funding=funding1[0].replace("\n", "").replace("\r","").replace("\t", "").strip()
    if funding == "-":
        funding = ""

    # 登记机关
    registrationAuthority1 = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[2]/text()')
    registrationAuthority=registrationAuthority1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if registrationAuthority == "-":
        registrationAuthority = ""

    # 有效期
    businessTerm1 = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[4]/text()')
    businessTerm=businessTerm1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if businessTerm == "-":
        businessTerm = ""


    # 企业地址
    address1 = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[2]/text()')
    address=address1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if address == "-":
        address = ""

    # 经营范围
    businessScope1 = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[2]/text()')
    businessScope=businessScope1[0].replace("\n", "").replace("\r", "").replace( "\t", "").strip()
    if businessScope == "-":
        businessScope = ""

    dic = {
        "_id":qcc_id,
        'entName': orgName,
        'taskId': taskId,
        'update_time': update_time,
        '基础信息': {
            'corporation': corporation,
            'orgLogo': orgLogo,
            'legalLink': legalLink,
            'legalCompanyNum': legalCompanyNum,
            'legalCompanyAdd': "[]",
            'enterpriseStatus': enterpriseStatus,
            'sponsor': sponsor,
            'creditCode': creditCode,
            'start_money': start_money,
            'businessTerm': businessTerm,
            'funding': funding,
            'registrationAuthority': registrationAuthority,
            'address': address,
            "businessScope": businessScope,
            'telphone': '',
            'email': '',
            'website': '',
            'introduction': ''
        }

    }
    print(dic)
    return dic
