import requests,re,json
from dao import Mysql
from lxml import etree
import time,datetime
now = int(time.time())
ts = int(datetime.datetime.now().timestamp() * 1000)


selects=Mysql.select_fujian()
for select1 in selects:
    url=select1[3]
    # url='http://220.160.52.164:96/ConstructionInfoPublish/Pages/CompanyQualificationInfo.aspx?companyID=125102&companyguid=4E73736A-E3C9-4C49-B880-2B6BBF271100%20&index=0&_=1595905906263'
    con_url=url.replace('CompanyInfo','CompanyQualificationInfo')+f'%20&index=0&_={ts}'
    content1=requests.get(con_url).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
    content=re.findall('<td>(.*?)</td>',content1)
    if content:
        intelligencetype = []
        zsh = content[0]
        zzfw = content[1].replace('</br>',',').replace(' ','')
        zzfw1 = zzfw.split(',')
        fzrq = content[4]
        zsyxq = content[5]
        fzjg = content[2]
        zzlx = select1[4]+'企业资质'
        if len(zzfw1) > 1:
            print('含有多个资质名称')
            for i in range(len(zzfw1)):
                if len(zzfw1[i])>0:
                    tt=select1[0]
                    zzmc = zzfw1[i]
                    select = Mysql.select_qyzz(qyid=select1[0], zzmc=zzmc)
                    if len(select) > 0:
                        print(f'数据已存在[{zsh}]')
                    else:
                        Mysql.insert_qyzz(qyid=select1[0], zzlx=zzlx, zsh=zsh, zzmc=zzmc, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg, zzfw=zzfw)
                        Mysql.update_fj(qyname=select1[1], qyurl=select1[3], zt=1)

        else:
            print('只有一个资质名称')
            zzmc=zzfw
            select = Mysql.select_qyzz(qyid=select1[0], zzmc=zzfw)
            if len(select) > 0:
                print(f'数据已存在[{zsh}]')
            else:
                Mysql.insert_qyzz(qyid=select1[0], zzlx=zzlx, zsh=zsh, zzmc=zzfw, fzrq=fzrq, zsyxq=zsyxq, fzjg=fzjg, zzfw=zzfw)
                Mysql.update_fj(qyname=select1[1],qyurl=select1[3],zt=1)


        igtype = [zzlx, zsh, zzfw,fzrq, zsyxq, fzjg]
        intelligencetype.append(igtype)

    print('fff')