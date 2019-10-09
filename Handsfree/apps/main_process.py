from selenium.webdriver.common.by import By

from apps.basic import DemoSum

from apps.file_data import SaveData


def file_data_startup():
    """
    数据文件准备
    :return: 数据实例化对象 obj
    """
    df = SaveData()
    df.read_file_data()  # 读取数据文件
    df.find_data_marks()  # 第一次读取时候，获取书记标记
    return df


def web_driver_startup():
    """
    冲浪初始化
    :return: 冲浪实例化对象 obj
    """
    carrier = DemoSum()
    carrier.chinese_login_page_start()
    return carrier


def login_process(carrier=None, data_obj=None):
    """登录"""
    login_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT'][@value=' Login ' or @value=' 登入 ']")
    login_btn = carrier.target_button_ready(locate=login_btn_locate)
    data_obj.get_user_info()
    carrier.login_step(username=data_obj.user_account[0], password=data_obj.user_account[1])
    login_btn.click()
    check_point = carrier.login_verify()
    if check_point is False:
        data_obj.save_account_error_mark()
        return False
    return True


def method_r_pin_stock(carrier=None, data_obj=None):
    """重消股模式"""
    carrier.buy_load_stocks_mode(data_frame=data_obj)
    # carrier.common_refresh()
    # trade_btn_locate = (By.XPATH, "//a[@class='GLink'][text()='交易']")
    # trade_btn = carrier.target_button_ready(trade_btn_locate)
    # trade_btn.click()
    # # step two
    # r_pin_btn_locate = (By.XPATH, "//a[contains(text(),'重消贷款')][contains(text(),'重消') or text()='买 (重消贷款)']")
    # r_pin_btn = carrier.target_button_ready(r_pin_btn_locate)
    # r_pin_btn.click()
    # # 进入交易流程，当前位置为交易数值输入（寻找‘下一步’跳转）
    # carrier.common_refresh()
    # next_btn_locate = (By.XPATH, "//input[@class='button'][@type='SUBMIT']")
    # carrier.buy_load_stocks(locate=next_btn_locate, data_frame=data_obj)
    # if carrier.stock_flag:
    #     carrier.common_refresh()  # 若点了下一步的情况，（寻找‘完成’跳转）
    #     complete_btn_locate = (By.XPATH, "//input[@class='button'][@type='BUTTON'][@onclick='Go()']")
    #     carrier.complete_buy_load_stocks(locate=complete_btn_locate, data_frame=data_obj)
    #     # 续上步，完成后页面判断
    #     carrier.common_refresh()
    # else:
    #     data_obj.record_data()


def method_cash_point(carrier=None, data_obj=None):
    """现金分模式"""
    # 进入钱包界面
    wallet_btn_locate = (By.XPATH, "/html/body/a[7]")
    carrier.entry_first_page_from_home(locate=wallet_btn_locate)

    # 奖金分转现金分
    price_to_cash_point_btn_locate = (By.XPATH, "/html/body/div[1]/ul/li[1]/a")
    carrier.cash_point_judge(locate=price_to_cash_point_btn_locate, data_frame=data_obj)

    if carrier.cash_point_flag:
        # 完成数值输入，点击下一步
        on_next_btn_locate = (By.XPATH, "/html/body/div[1]/table/tbody/tr[8]/td/input[2]")
        carrier.cash_point_process(locate=on_next_btn_locate, data_frame=data_obj)

        # 交易完成
        complete_btn_locate = (By.XPATH, "//*[@id='Submit']/input[2]")
        carrier.cash_point_trade_finish(locate=complete_btn_locate, data_frame=data_obj)

        carrier.last_check()
    # 等待页面刷新
    # 或许页面数据，并判断
    # 若达标，则进入下一步交易，点击
        # 进入后
        # (By.XPATH, "/html/body/div[1]/ul/li[5]/a")
        # 判断是否有弄太子支付
        # (By.XPATH, "/html/body/div[1]/font/b")  # 有故障，交易失败


def logout_process(carrier=None, data_obj=None):
    """登出"""
    carrier.logout_account(data_frame=data_obj)


def method_taizi_account_set(carrier=None, data_frame=None):
    """太子手机账号绑定"""
    check_point_1 = carrier.enter_setting(data_frame=data_frame)
    if check_point_1 is False:
        data_frame.save_secondary_password_error()
        return
    carrier.get_phone_number(data_frame=data_frame)


def method_force_taizi_account_set(carrier=None, data_frame=None):
    """太子手机账号绑定"""
    check_point_1 = carrier.f_enter_setting(data_frame=data_frame)
    if check_point_1 is False:
        data_frame.save_secondary_password_error()
        return
    carrier.f_get_phone_number(data_frame=data_frame)


def method_cash_point_transfer_taizhi(carrier=None, data_frame=None):
    """现金分转太子提现"""
    carrier.cash_point_to_taizhi(data_frame=data_frame)


def method_information_record(carrier=None, data_frame=None):
    """记录用户信息"""
    carrier.register_time(data_frame=data_frame)


def method_sell_stock(carrier=None, data_frame=None):
    """卖股流程"""
    carrier.sell_stock(data_frame=data_frame)
