from selenium.webdriver.common.by import By

from apps.basic import DemoSum

from apps.file_data import FilesData


def file_data_startup():
    """
    数据文件准备
    :return: 数据实例化对象 obj
    """
    df = FilesData()
    df.read_file_data()  # 读取数据文件
    df.find_data_marks()  # 第一次读取时候，获取书记标记
    return df


def web_driver_startup():
    """
    冲浪初始化
    :return: 冲浪实例化对象 obj
    """
    carrier = DemoSum()
    carrier.get_url()
    return carrier


def login_process(carrier=None, data_obj=None):
    """登录"""
    login_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT'][@value=' Login ']")
    login_btn = carrier.target_button_ready(locate=login_btn_locate)
    data_obj.get_user_info()
    carrier.login_step(username=data_obj.user_account[0], password=data_obj.user_account[1])
    login_btn.click()


def method_r_pin_stock(carrier=None, data_obj=None):
    """重消股模式"""
    carrier.common_refresh()
    trade_btn_locate = (By.XPATH, "//a[@class='GLink'][text()='交易']")
    trade_btn = carrier.target_button_ready(trade_btn_locate)
    trade_btn.click()
    # step two
    r_pin_btn_locate = (By.XPATH, "//a[contains(text(),'重消贷款')][contains(text(),'重消') or text()='买 (重消贷款)']")
    r_pin_btn = carrier.target_button_ready(r_pin_btn_locate)
    r_pin_btn.click()
    # 进入交易流程，当前位置为交易数值输入（寻找‘下一步’跳转）
    carrier.common_refresh()
    next_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT']")
    carrier.buy_load_stocks(locate=next_btn_locate, data_frame=data_obj)
    if carrier.stock_flag:
        carrier.common_refresh()  # 若点了下一步的情况，（寻找‘完成’跳转）
        complete_btn_locate = (By.XPATH, "//input[@class='button'][@type='BUTTON'][@onclick='Go()']")
        carrier.complete_buy_load_stocks(locate=complete_btn_locate, data_frame=data_obj)
        # 续上步，完成后页面判断
        carrier.common_refresh()
    else:
        data_obj.record_data()


def logout_process(carrier=None, data_obj=None):
    """登出"""
    logout_btn_locate = (By.XPATH, "//a[@class='GLink'][contains(text(),'退出')]")
    carrier.logout_account(locate=logout_btn_locate, data_frame=data_obj)
