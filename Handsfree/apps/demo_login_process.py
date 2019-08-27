from selenium.webdriver.common.by import By

from apps.basic import DemoSum
from apps.main_process import file_data_startup, web_driver_startup


def main_login_step():
    # 1.打开浏览器并获取登录页面数据
    browser_truck = web_driver_startup()
    file_data = file_data_startup()
    login_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT'][@value=' Login ' or @value=' 登入 ']")
    login_btn = browser_truck.target_button_ready(locate=login_btn_locate)
    file_data.get_user_info()
    browser_truck.login_step(username=file_data.user_account[0], password=file_data.user_account[1])
    login_btn.click()
    browser_truck.common_refresh()
    cookie = browser_truck.driver.get_cookies()
    print(cookie)

    # 2.确定验证码刷新后，输入数据登录
    # 3.判断账号是否登录成功
    # 4.登录成功，获取需要数据

main_login_step()
