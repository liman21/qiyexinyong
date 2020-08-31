# -*- coding: utf-8 -*-
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的
import asyncio
import random,time
from dao import Mysql
import json


# 获取登录后cookie
async def get_cookie(page):
    cookies_list = await page.cookies()
    # print(cookies_list)
    # cookies = ''
    # for cookie in cookies_list:
    #     str_cookie = '{0}={1};'
    #     str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
    #     cookies += str_cookie
    # # print(cookie)
    # return cookies
    cookies = {}
    for item in cookies_list:
        cookies[item["name"]] = item["value"]
    print("the cookie is {}".format(cookies))
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键

        await page.mouse.move(random.randint(300,500),random.randint(400,800),{'steps':10,'delay': random.randint(10,50)})
        # await asyncio.sleep(0.5)
        # await page.mouse.move(-random.randint(300,500),-random.randint(400,800))
        # await page.mouse.click(random.randint(300,500),random.randint(400,800))
        await asyncio.sleep(0.5)
        await page.hover(".nc-lang-cnt ")

        await page.mouse.down()
        await asyncio.sleep(0.5)
        # await page.mouse.move(1000, 10, {'delay': random.randint(10,20),'steps':2})
        await page.mouse.move(random.randint(2500,2800), 10,{'delay': random.randint(10,50)})
        await asyncio.sleep(random.randint(1, 2))
        await page.mouse.up()

        req_text = await page.content()

        if '验证通过' in req_text:
            return True

        flush_a = await page.xpath('//div[@id="dom_id_one"]//a')
        if not flush_a:
            flush_a = await page.xpath('//div[@id="dom_id"]//a')
        await flush_a[0].click()
        return False

    except Exception as e:
        print(e)
        return False

def input_time_random():
    return random.randint(100, 151)

async def main(url,username,pwd):
    browser = await launch({
        'headless': False,
        # 'args': [f'--window-size={2200}, {1000}']})
        'args': [f'--window-size={width},{height}']})
    # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面

    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36')


    await page.goto(url)  # 访问登录页面
    await asyncio.sleep(1)

    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')


    # 使用type选定页面元素，并修改其数值，用于输入账号密码，修改的速度仿人类操作，因为有个输入速度的检测机制
    # 因为 pyppeteer 框架需要转换为js操作，而js和python的类型定义不同，所以写法与参数要用字典，类型导入
    await page.setViewport({"width": 1920, "height": 895})
    print('103')
    await page.click("#normalLogin")

    await asyncio.sleep(0.5)
    await page.mouse.move(random.randint(1, 10), random.randint(19, 50))
    await page.type('#nameNormal', username, {'delay': input_time_random() - 150})
    await page.type('#pwdNormal', pwd, {'delay': input_time_random()})
    print("---------------------开始拉动------------------------------------------")
    await asyncio.sleep(1)
    # await page.mouse.move(random.randint(1, 10), random.randint(19, 50))

    # js拉动滑块过去。
    # result = await mouse_slide(page=page,id_xpath='.nc-lang-cnt')
    count = 4
    while count:
        await asyncio.sleep(0.5)
        result = await mouse_slide(page=page)
        count -= 1
        if result:
            count = True
            break

    # await page.screenshot({'path': './headless-login-slide.png'})  # 截图测试

    if not count:
        print("----------------------------验证失败----------------------------------------")
        return None

    await asyncio.sleep(1)

    button_loggin = await page.xpath('//form[@id="user_login_normal"]/button')
    await button_loggin[0].click()

    if not count:
        print("----------------------------验证失败----------------------------------------")
        await page.close()
        await browser.close()
        return None

    print("----------------------------验证成功----------------------------------------")

    cookies = await get_cookie(page)
    cookie = json.dumps({username:cookies}) + '\n'
    print('=======================cookie如下=========================')
    # with open("cookies_bendi1.txt", "w") as f:
    #     f.write(json.dumps({username:cookies}) + '\n')
    Mysql.insert_qycookie(cookie=cookie)



    print('==========================================================')
    await page.close()
    await browser.close()



# 开启协诚
url = 'https://www.qichacha.com/user_login'
# queue = ['15028362124_a123456',]
# queue = ['15511091561_123456',]
# queue = ["13644369603_a123456","15886194139_a123456","15143582394_a123456","15844559746_a123456","15081452609_a123456","15032980247_a123456","15230902124_a123456",]
width, height = 2200, 1000
loop = asyncio.get_event_loop()
line = ""

# with open("data.txt", "r") as f:
#     line = f.readlines()
# aclist = []
# for x in line:
#     aclist.append(x.strip())
# print(aclist)
# i = 0
# for x in aclist:
#     username = x.split("_")[0]
#     pwd= x.split("_")[1]
while True:
    try:
        loop.run_until_complete(main(url=url, username='15733188662', pwd='123456'))
    except:
        continue


