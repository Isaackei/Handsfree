from selenium.webdriver.common.by import By

from apps.basic import DemoSum
# load data
from apps.file_data import FilesData

# 数据读取及准备
data_obj = FilesData()
data_obj.read_file_data()  # 读取数据文件
data_obj.find_data_marks()  # 第一次读取时候，获取书记标记

for i in range(20):
    data_obj.get_user_info()  # 获取当前用户账号密码

    # login
    walker = DemoSum()
    walker.get_url()
    login_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT'][@value=' Login ']")
    login_btn = walker.target_button_ready(login_btn_locate)
    walker.login_process(username=data_obj.user_account[0], password=data_obj.user_account[1])
    login_btn.click()

    # stock mode A
    walker.common_refresh()
    trade_btn_locate = (By.XPATH, "//a[@class='GLink'][text()='交易']")
    trade_btn = walker.target_button_ready(trade_btn_locate)
    trade_btn.click()
    # stock mode A step two
    R_pin_btn_locate = (By.XPATH, "//a[contains(text(),'重消贷款')][contains(text(),'重消') or text()='买 (重消贷款)']")
    R_pin_btn = walker.target_button_ready(R_pin_btn_locate)
    R_pin_btn.click()
    # 进入交易流程，当前位置为交易数值输入（寻找‘下一步’跳转）
    walker.common_refresh()
    next_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT']")
    walker.buy_load_stocks(locate=next_btn_locate, data_frame=data_obj)

    # 若点了下一步的情况，（寻找‘完成’跳转）
    walker.common_refresh()
    complete_btn_locate = (By.XPATH, "//input[@class='button'][@type='BUTTON'][@onclick='Go()']")
    walker.complete_buy_load_stocks(locate=complete_btn_locate, data_frame=data_obj)

    # 续上步，完成后页面判断
    walker.common_refresh()

    # 登出账号
    logout_btn_locate = (By.XPATH, "//a[@class='GLink'][contains(text(),'退出')]")
    walker.logout(locate=logout_btn_locate, data_frame=data_obj)


