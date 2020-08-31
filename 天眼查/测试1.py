# coding=utf-8
from selenium import webdriver
import time
from PIL import Image, ImageGrab
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains

'''
用于天眼查自动登录，解决滑块验证问题
'''


def get_track(distance):
    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 2 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 50

    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 5
        else:
            # 加速度为负3
            a = -2
        # 初速度v0
        v0 = v
        # 当前速度v = v0 + at
        v = v0 + a * t
        # 移动距离x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track


def autologin(account, password):
    driver.get('https://www.tianyancha.com')
    time.sleep(3)
    js = 'Object.defineProperties(navigator,{webdriver:{get:() => false}});'
    js_1 = '() =>{ window.navigator.chrome = { runtime: {},  }; }'
    js_2 = '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }'''
    js_3 = '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }'''
    driver.execute_script(js)  # 运行JS跳过浏览器检测
    driver.execute_script(js_1)  # 运行JS跳过浏览器检测
    driver.execute_script(js_2)  # 运行JS跳过浏览器检测
    driver.execute_script(js_3)  # 运行JS跳过浏览器检测
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="web-content"]/div/div[1]/div[1]/div/div/div[2]/div/div[5]/a').click()  # 登录注册
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[2]').click()  # 密码注册
    time.sleep(1)
    email = driver.find_element_by_xpath('//*[@id="mobile"]')
    passwords = driver.find_element_by_xpath('//*[@id="password"]')
    email.send_keys(account)
    passwords.send_keys(password)

    driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/div[2]').click()  # 登录
    # 点击登录之后开始截取验证码图片
    time.sleep(2)
    img = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div[1]')
    time.sleep(0.5)
    # 获取图片位子和宽高
    location = img.location
    size = img.size
    # 返回左上角和右下角的坐标来截取图片
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
    # 截取第一张图片(无缺口的)
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha1 = screenshot.crop((left, top, right, bottom))
    print('--->', captcha1.size)
    captcha1.save('captcha1.png')
    # 截取第二张图片(有缺口的)
    driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]').click()
    time.sleep(4)
    img1 = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div[1]')
    time.sleep(0.5)
    location1 = img1.location
    size1 = img1.size
    top1, bottom1, left1, right1 = location1['y'], location1['y'] + size1['height'], location1['x'], location1['x'] + \
                                   size1['width']
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha2 = screenshot.crop((left1, top1, right1, bottom1))
    captcha2.save('captcha2.png')
    # 获取偏移量
    left = 55  # 这个是去掉开始的一部分
    for i in range(left, captcha1.size[0]):
        for j in range(captcha1.size[1]):
            # 判断两个像素点是否相同
            pixel1 = captcha1.load()[i, j]
            pixel2 = captcha2.load()[i, j]
            threshold = 60
            if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                    pixel1[2] - pixel2[2]) < threshold:
                pass
            else:
                left = i
    print('缺口位置', left)
    # 减去缺口位移
    left -= 54
    # 开始移动
    track = get_track(left)
    print('滑动轨迹', track)
    track += [5, -5, 2, -2]  # 滑过去再滑过来，不然有可能被吃
    # 拖动滑块
    slider = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]')
    ActionChains(driver).click_and_hold(slider).perform()
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    ActionChains(driver).release().perform()
    time.sleep(2)
    try:
        if driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]'):
            print('能找到滑块，重新试')
            driver.delete_all_cookies()
            driver.refresh()
            autologin(account, password)
        else:
            print('login success')
    except:
        print('login success')


if __name__ == '__main__':
    # chromeoption = webdriver.ChromeOptions()
    # chromeoption.add_argument('--headless')
    # chromeoption.add_argument('user-agent='+user_agent)
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    account = '15133700854'
    password = 'wk1996..'
    autologin(account, password)
