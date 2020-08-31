from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


# 滑动验证码识别
def slide_discern():
    print("滑块验证码验证中。。。")
#创建无界面模式

    url = 'https://www.qichacha.com/user_login'

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.find_element_by_xpath("//a[@id='normalLogin']").click()
    driver.find_element_by_id('nameNormal').send_keys('17195453625')
    driver.find_element_by_id('pwdNormal').send_keys('123456')
    driver.find_element_by_xpath("//form[@id='user_login_normal']/button[@class='btn btn-primary btn-block m-t-md login-btn']").click()

    time.sleep(1)
# 获取到需滑动的按钮

    source = driver.find_element_by_id("nc_2_n1z")
    action = ActionChains(driver)
    # 按住左键不放
    action.click_and_hold(source).perform()
    # 开始滑动
    distance = 340
# 模拟以人为速度拖动
    track = get_track(distance)
    for i in track:
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        action.reset_actions()
    # 释放鼠标
    action.release().perform()




try:
    slide_discern()
except Exception as e:
    print(e)
    print('d')