import time, hashlib, re
from lxml import etree
from dao import Mysql


def extra_same_elem(lst, *lsts):
    iset = set(lst)
    for li in lsts:
        s = set(li)
        iset = iset.intersection(s)
    return list(iset)



def get_data(html,qcc_id,orgName,content):
    # 简介
    jianjie1 = html.xpath('//*[@id="jianjieModal"]/div/div/div[2]/div/pre/text()')
    if jianjie1 != []:
        jianjie = jianjie1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()

    else:
        jianjie = ""
    print(jianjie)
    taskId = hashlib.md5(orgName.encode(encoding='UTF-8')).hexdigest()
    update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))

    orgLogo1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[2]/div/div/div[1]/img')
    if orgLogo1:
        orgLogo = orgLogo1[0].get("src")
    else:
        orgLogo = ""

    # 法人
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


    # 成立日期

    regDate1 = html.xpath('//*[@id="Cominfo"]/table/tr[1]/td[6]/text()')
    regDate=regDate1[0].replace("\n", "").replace("\r","").replace( "\t", "").strip()
    if regDate == "-":
        regDate = ''

    # 注册资本

    regCapital1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[2]/text()')
    regCapital=regCapital1[0].strip().replace("\n", "").replace("\r", "").replace("\t", "")
    if regCapital == "-":
        regCapital = ""

    # 实缴资本

    contributedcapital1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[4]/text()')
    contributedcapital=contributedcapital1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if contributedcapital == "-":
        contributedcapital = ""

    # 核准日期
    checkDate1 = html.xpath('//*[@id="Cominfo"]/table/tr[2]/td[6]/text()')
    checkDate=checkDate1[0].replace("\n", "").replace("\r","").replace("\t", "").strip()
    if checkDate == "-":
        checkDate = ""

    # 统一社会信用代码
    creditCode1 = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[2]/text()')
    creditCode=creditCode1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if creditCode == "-":
        creditCode = ""
    # 组织机构代码
    orgCode1 = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[4]/text()')
    orgCode=orgCode1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if orgCode == "-":
        orgCode = ""
    # 工商注册号
    businessRegCode1 = html.xpath('//*[@id="Cominfo"]/table/tr[3]/td[6]/text()')
    businessRegCode=businessRegCode1[0].replace("\n", "").replace("\r","").replace("\t", "").strip()
    if businessRegCode == "-":
        businessRegCode = ""
    # 纳税人识别号
    taxpayerIdNo = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[2]/text()')[0].replace("\n", "").replace("\r",
                                                                                                          "").replace(
        "\t", "").strip()
    if taxpayerIdNo == "-":
        taxpayerIdNo = ""

    # 进出口企业代码
    taxpayerQualification = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[4]/text()')[0].replace("\n", "").replace(
        "\r", "").replace("\t", "").strip()
    if taxpayerQualification == "-":
        taxpayerQualification = ""
    # 所属行业
    industry = html.xpath('//*[@id="Cominfo"]/table/tr[4]/td[6]/text()')[0].replace("\n", "").replace("\r",
                                                                                                      "").replace(
        "\t", "").strip()
    if industry == "-":
        industry = ""
    # 企业类型
    enterpriseType = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[2]/text()')[0].replace("\n", "").replace("\r",
                                                                                                            "").replace(
        "\t", "").strip()
    if enterpriseType == "-":
        enterpriseType = ""
    # 营业期限
    businessTerm1 = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[4]/text()')
    businessTerm = businessTerm1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if businessTerm == "- 至 -" or businessTerm == "-":
        businessTerm = ""
    print("businessTerm", businessTerm)
    # 登记机关
    registrationAuthority = html.xpath('//*[@id="Cominfo"]/table/tr[5]/td[6]/text()')[0].replace("\n", "").replace(
        "\r", "").replace("\t", "").strip()
    if registrationAuthority == "-":
        registrationAuthority = ""
    # 人员规模
    staffSize = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[2]/text()')[0].replace("\n", "").replace(
        "\r", "").replace("\t", "").strip()
    if staffSize == "-":
        staffSize = ""
    # 参保人数
    contributors = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[4]/text()')[0].replace("\n", "").replace("\r",
                                                                                                          "").replace(
        "\t", "").strip()
    if contributors == "-":
        contributors = ""
    # 所属地区
    city = html.xpath('//*[@id="Cominfo"]/table/tr[6]/td[6]/text()')[0].replace("\n", "").replace("\r", "").replace(
        "\t", "").strip()
    if city == "-":
        city = ""

    # 曾用名
    try:
        oldOrgName1 = html.xpath('//section[@id="Cominfo"]/table[@class="ntable"]/tr[7]/td[2]/span/text()')
        if len(oldOrgName1)>1:
            print("两个曾用名")
            oldOrgName2 = oldOrgName1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
            oldOrgName3 = oldOrgName1[1].replace("\n", "").replace("\r", "").replace("\t", "").strip()
            oldOrgName=oldOrgName2 + "," +oldOrgName3
        else:
            oldOrgName=oldOrgName1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    except Exception:
        oldOrgName=""
        print("没有曾用名")
    print("oldOrgName1", oldOrgName)
    if oldOrgName == "-":
        oldOrgName = ""
    # 英文名
    orgNameEn = html.xpath('//*[@id="Cominfo"]/table/tr[7]/td[4]/text()')[0].replace("\n", "").replace("\r","").replace("\t", "").strip()
    if orgNameEn == "-":
        orgNameEn = ""

    # 企业地址
    address1 = html.xpath('//*[@id="Cominfo"]/table/tr[8]/td[2]/text()')
    address = address1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    if address == "-":
        address = ""

    # 经营范围
    # businessScope1 = html.xpath('//*[@id="Cominfo"]/table/tr[9]/td[2]/text()')
    # businessScope = businessScope1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()
    # if businessScope == "-":
    #     businessScope = ""

    # 企业资质
    # intelligencetype1 = html.xpath("//*[@id=\"bmqualificationlist\"]/text()")
    # intelligencetype = intelligencetype1[0].replace("\n", "").replace("\r", "").replace("\t", "").strip()


    intelligencetype1 = re.findall('<tr> <td class="tx">(\d+)</td> <td width="150" class="text-left">(.*?)</td> <td width="135" class="text-left"> <a onclick="(.*?)\)">(.*?)</a> </td> <td>(.*?)</td> <td width="104" class="text-center">(.*?)</td> <td width="104" class="text-center">(.*?)</td> <td width="104" class="text-left">(.*?)</td> </tr>',content)
    if len(intelligencetype1)>0:
        intelligencetype = []
        for intelligencetypes in intelligencetype1:
            zzlx=intelligencetypes[1].strip()
            zsh=intelligencetypes[3]
            zzfw=intelligencetypes[4]
            zzfw1=intelligencetypes[4].split(',')
            fzrq = intelligencetypes[5]
            zsyxq = intelligencetypes[6]
            fzjg = intelligencetypes[7]
            igtype = [zzlx, zsh, zzfw, fzrq, zsyxq, fzjg]
            intelligencetype.append(igtype)
            if len(zzfw1)>1:
                print('含有多个资质名称')
                for i in range(len(zzfw1)):
                    zzmc=zzfw1[i]
                    select = Mysql.select_qyzz(qyid=qcc_id, zzmc=zzmc)
                    if len(select) > 0:
                        print(f'数据已存在[{zsh}]')
                    else:
                        Mysql.insert_qyzz(qyid=qcc_id, zzlx=zzlx, zsh=zsh, zzmc=zzmc, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg,
                                          zzfw=zzfw)
            else:
                select = Mysql.select_qyzz(qyid=qcc_id, zzmc=zzfw)
                if len(select) > 0:
                    print(f'数据已存在[{zsh}]')
                else:
                    Mysql.insert_qyzz(qyid=qcc_id, zzlx=zzlx, zsh=zsh, zzmc=zzfw, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg,
                                  zzfw=zzfw)



        dic1 = {
            '基础信息': {
                'regCapital': regCapital,
                'enterpriseType': enterpriseType,
                'businessTerm': businessTerm,
                'intelligencetype': intelligencetype
            }
        }
        print(dic1)

        return dic1
    else:
        pass
    intelligencetype=66
    # if intelligencetype == "-":
    #     intelligencetype = ""

    dic = {
        "_id":qcc_id,
        'entName': orgName,
        'taskId': taskId,
        'update_time': update_time,
        '基础信息': {
            'telphone': "",
            'email': "",
            'website': "",
            'introduction': jianjie,
            'corporation': corporation,
            'legalLink': legalLink,
            'legalCompanyNum': legalCompanyNum,
            'orgLogo': orgLogo,
            'enterpriseStatus': enterpriseStatus,
            'regDate': regDate,
            'regCapital': regCapital,
            "contributedcapital": contributedcapital,
            'checkDate': checkDate,
            'creditCode': creditCode,
            'orgCode': orgCode,
            'businessRegCode': businessRegCode,
            'taxpayerIdNo': taxpayerIdNo,
            'taxpayerQualification': taxpayerQualification,
            'industry': industry,
            'enterpriseType': enterpriseType,
            'businessTerm': businessTerm,
            'registrationAuthority': registrationAuthority,
            'staffSize': staffSize,
            'contributors': contributors,
            "city": city,
            'oldOrgName': oldOrgName,
            'orgNameEn': orgNameEn,
            'address': address,
            'intelligencetype': intelligencetype,
        }
    }


