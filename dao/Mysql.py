from utils import util, dbmysql
import time
import uuid

# # 查询有没有uid
def select_xinwen(**kwargs):
    rs = None
    try:
        sql = "select * from xinwen_baseinfo where title='%s';" % (kwargs["title"])
        rs = dbmysql.fetchall(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs


# # #插入招标文件  *项目名称 ,工程类型,立项文件号,开标日期格式 , 保函申请开始时间 , 电子保函申请截止时间, 预计造价（元）,计划工期（天）, 建设地点 ,投标资质等级要求 , *保证金金额（元）,招标单位名称，*社会信用代码，营业期限, 地址, 联系人， 电话
# def insert_xinwen_baseinfo(**kwargs):
#     try:
#         insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#         sql = "insert into xinwen_baseinfo (uid,regionCode,regionName,areaRegion,publicTime,linkurl,title,dataResource,yewuType,infoType,infoState,insertDBtime)" \
#               "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (kwargs["uid"],kwargs["regionCode"],kwargs["regionName"],kwargs["areaRegion"],kwargs["publicTime"],kwargs["linkurl"],kwargs["title"],kwargs["dataResource"],kwargs["yewuType"],kwargs["infoType"],kwargs["infoState"],insertDBtime)
#         sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
#         dbmysql.execute(sql=sql)
#     except Exception as e:
#         print('蚌埠\t', e)
#         return 404
#
#
#
#
# def insert_xinwen_detailinfo(**kwargs):
#     try:
#         sql = "insert into xinwen_detailinfo (uid,infocontent) value ('%s','%s');" % (kwargs['uid'], kwargs['infocontent'])
#         sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
#         dbmysql.execute(sql=sql)
#     except Exception as e:
#         print('蚌埠\t', e)
#         return 404


def update_xmxq2(**kwargs):
    rs = None
    try:
        sql = "update xmxq set yyqx='%s'where zbdwmc ='%s' "% (kwargs["yyqx"], kwargs["zbdwmc"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)
    except Exception as e:
        util.logger.error(e)
    return rs


def updatexmxq_zt(**kwargs):
    rs = None
    try:
        sql = "update xmxq set finish='%s'where xmmc ='%s'and gclx ='%s';" % (
        kwargs["finish"], kwargs["xmmc"], kwargs["gclx"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)

    except Exception as e:
        util.logger.error(e)
        return rs
def updatexmxq_doc(**kwargs):
    rs = None
    try:
        sql = "update xmxq set doc_link='%s'where xmmc ='%s'and gclx ='%s';" % (
        kwargs["doc_link"], kwargs["xmmc"], kwargs["gclx"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)

    except Exception as e:
        util.logger.error(e)
        return rs

# # 查询有没有uid
def select_xw_nr(**kwargs):
    rs = None
    try:
        sql = f"select * from xw_nr where biaoti='{kwargs['biaoti']}';"
        rs = dbmysql.first(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs


# # 查询有没有uid
def select_fj(**kwargs):
    rs = None
    try:

        sql = f"select * from tbl_fj where qyname='{kwargs['qyname']}' and qyurl='{kwargs['qyurl']}';"
        rs = dbmysql.first(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs
def insert_fj(**kwargs):
    try:
        # insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        uid = uuid.uuid4()
        sql = "insert into tbl_fj (uid,qyname,shxydm,qyurl,zzlx,zt) value ('%s','%s','%s','%s','%s','0');" % (uid, kwargs['qyname'],kwargs['shxydm'], kwargs['qyurl'],kwargs['zzlx'])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        dbmysql.execute(sql=sql)
        # print(sql)
    except Exception as e:
        return 404

def update_fj(**kwargs):
    rs = None
    try:
        sql = "update tbl_fj set zt='%s'where qyname ='%s'and qyurl ='%s';" % (
        kwargs["zt"], kwargs["qyname"], kwargs["qyurl"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)

    except Exception as e:
        util.logger.error(e)
        return rs

# # 查询有没有uid
def select_xw(**kwargs):
    rs = None
    try:
        sql = f"SELECT * FROM `bh_gl`.`xw_nr` WHERE `zt` = '1' ORDER BY `biaoti` DESC;"
        rs = dbmysql.query(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs


def insert_xw_nr(**kwargs):
    try:
        # insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # sql = f"insert into xw_nr (prid,shengfen,dijishi,fabutime,url,biaoti,tianjiatime,zt) values ({kwargs['prid']},{kwargs['shengfen']},{kwargs['dijishi']},{kwargs['fabutime']},{kwargs['url']},{kwargs['biaoti']},{kwargs['tianjiatime']},'0')"
        sql = "insert into xw_nr (prid,shengfen,dijishi,fabutime,url,biaoti,tianjiatime,zt,xz,jtxz,xy) value ('%s','%s','%s','%s','%s','%s','%s','%s','0','0','0');" % (kwargs['prid'], kwargs['shengfen'],kwargs['dijishi'], kwargs['fabutime'],kwargs['url'], kwargs['biaoti'],kwargs['tianjiatime'], kwargs['zt'])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        dbmysql.execute(sql=sql)
        # print(sql)
    except Exception as e:
        return 404

def insert_qyzz(**kwargs):
    try:
        # insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # sql = f"insert into xw_nr (prid,shengfen,dijishi,fabutime,url,biaoti,tianjiatime,zt) values ({kwargs['prid']},{kwargs['shengfen']},{kwargs['dijishi']},{kwargs['fabutime']},{kwargs['url']},{kwargs['biaoti']},{kwargs['tianjiatime']},'0')"
        sql = "insert into tbl_qy_zz (qyid,zzlx,zsh,zzmc,fzrq,zsyxq,fzjg,zzfw) value ('%s','%s','%s','%s','%s','%s','%s','%s');" % (kwargs['qyid'], kwargs['zzlx'],kwargs['zsh'], kwargs['zzmc'],kwargs['fzrq'], kwargs['zsyxq'],kwargs['fzjg'], kwargs['zzfw'])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        dbmysql.execute(sql=sql)
        # print(sql)
    except Exception as e:
        return 404

def insert_qycookie(**kwargs):
    try:
        # insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        uid = uuid.uuid4()
        # sql = f"insert into xw_nr (prid,shengfen,dijishi,fabutime,url,biaoti,tianjiatime,zt) values ({kwargs['prid']},{kwargs['shengfen']},{kwargs['dijishi']},{kwargs['fabutime']},{kwargs['url']},{kwargs['biaoti']},{kwargs['tianjiatime']},'0')"
        sql = "insert into ipo_title (uid,cookie,zt) value ('%s','%s','%s');" % (uid, kwargs['cookie'],'0')
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        dbmysql.execute(sql=sql)
        # print(sql)
    except Exception as e:
        return 404
# # 查询有没有uid
def select_qyzz(**kwargs):
    rs = None
    try:
        sql =  f"select zzmc from tbl_qy_zz where qyid='{kwargs['qyid']}' and zsh ='{kwargs['zsh']}' and zzmc !='{kwargs['zzmc']}';"
        rs = dbmysql.fetchall(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs
# # 查询有没有uid
def select_qyzz(**kwargs):
    rs = None
    try:
        sql =  f"select zzmc from tbl_qy_zz where qyid='{kwargs['qyid']}' and zzmc ='{kwargs['zzmc']}';"
        rs = dbmysql.fetchall(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs
# # 查询有没有uid
def select_qycookie(**kwargs):
    rs = None
    try:
        sql =  f"select * from ipo_title where zt='0';"
        rs = dbmysql.first(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs

def update_qyzz(**kwargs):
    rs = None
    try:
        sql = "update zzfw set zsh='%s' where tbl_qy_zz ='%s' "% (kwargs["zzfw"], kwargs["zsh"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)
        print(sql)
    except Exception as e:
        util.logger.error(e)

def delete_qycookie(**kwargs):
    rs = None
    try:
        sql = "delete from ipo_title where uid='%s'"% (kwargs["uid"])
        sql = sql.replace('\\', '-').replace('\n', '').replace('\r', '').replace('\t', '')
        rs = dbmysql.query(sql)
    except Exception as e:
        util.logger.error(e)


# # 查询有没有uid
def select_fujian(**kwargs):
    rs = None
    try:
        sql = f"SELECT * FROM `ceshi`.`tbl_fj` WHERE `zt` = '0' ORDER BY `uid`;"
        rs = dbmysql.fetchall(sql)
        return rs
    except Exception as e:
        util.logger.error(e)
        return rs
