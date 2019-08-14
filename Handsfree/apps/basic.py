import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

from settings.settings import DRIVER, URL, TOTAL_NUMBER_OF_REFRESH


class Basic(object):
    """
    浏览器初始化及基本配置准备
    """
    def __init__(self):
        self.star_driver = DRIVER
        self.driver = None
        self.main_url = URL
        self.target_elements = None
        self.common_elements = EC.presence_of_element_located((By.XPATH, "//div[@class='Footer']"))
        # self.url_list = []

    def common_page_ready(self):
        """
        判断页面加载情况
        判断一次加载情况
        :return: True or False bool
        """
        try:
            WebDriverWait(self.driver, 10).until(
                self.common_elements)
            return True
        except:
            return False

    def common_refresh(self):
        """
        普通页面加载失败刷新
        判断多次加载情况
        """
        refresh_count = 0
        while refresh_count < TOTAL_NUMBER_OF_REFRESH:
            if self.common_page_ready() is False:
                self.driver.refresh()
                refresh_count += 1
            else:
                # current_url_tmp = self.driver.current_url
                # if current_url_tmp not in self.url_list:
                #     self.url_list.append(current_url_tmp)
                break

    def get_url(self):
        """
        前往指定网页
        并执行页面刷新判断
        """
        self.driver = webdriver.Chrome(self.star_driver)
        self.driver.get(self.main_url)
        self.common_refresh()


class ButtonMixin(Basic):

    def target_button_ready(self, locate=None):
        """
        判断目标按钮加载情况
        :param locate: 目标定位的方法及路径，元祖，例如（By.XPATH, "//input[@class='btn']"）
        :return: 成功获取后返回按钮对象
        """
        refresh_count = 0
        while refresh_count < TOTAL_NUMBER_OF_REFRESH:
            print("target_button_ready")
            try:
                button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locate))
                if button:
                    print("get")
                    return button
            except:
                self.driver.refresh()
                refresh_count += 1


class LoginMixin(Basic):
    """针对页面登录"""

    def verify_code_input(self):
        """验证码输入"""
        while True:
            verify_code_list = []
            compare_number = "123456"
            count_diff = 0
            for index in range(1, 7):
                num_n = self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
                verify_code_list.append(num_n)
                if num_n != compare_number[index - 1]:
                    count_diff += 1

            if count_diff > 0:
                break
        # 第二次获取验证码，预防延迟
        verify_code_real = ""
        for index in range(1, 7):
            verify_code_real += self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
        self.driver.find_element_by_css_selector("[name='SKey']").send_keys(verify_code_real)

    def account_input(self, username=None, password=None):
        """账号密码输入"""
        self.driver.find_element_by_css_selector("td>input").send_keys(username)
        self.driver.find_element_by_css_selector("[type='password']").send_keys(password)

    def login_step(self, username=None, password=None):
        """集合登录流程"""
        self.account_input(username=username, password=password)
        self.verify_code_input()


class StockModeAMixin(ButtonMixin):
    """重消股"""
    def __init__(self):
        super().__init__()
        self.stock_flag = False
        self.stock_value = None

    def complete_buy_load_stocks(self, locate=None, data_frame=None):
        """完成重消股购买，并记录数据"""
        self.target_button_ready(locate).click()
        data_frame.record_data()

    def stock_judge(self, locate=None):
        """判断数值是否达标"""
        self.stock_flag = False
        if float(self.stock_value) > 2:
            self.stock_flag = True
            self.target_button_ready(locate).click()

    def buy_load_stocks(self, locate=None, data_frame=None):
        """重消股初步交易操作"""
        elements = self.driver.find_element_by_xpath("//input[@type='TEXT' and @name='Amount']")
        # 重消股数量
        stock_values = elements.get_attribute('value')
        # 判断是否为数值
        try:
            self.stock_value = "%.2f" % float(stock_values)
        except:
            self.stock_value = 0
        finally:
            data_frame.stock_R_pin = self.stock_value  # 将股票数记录为数据对象的股票数属性

        self.stock_judge(locate=locate)


class LogoutMixin(ButtonMixin):
    def logout_account(self, locate=None, data_frame=None):
        data_frame.final_record_data()
        self.target_button_ready(locate).click()
        self.common_refresh()
        # 写死最后退出元素定位
        btn_locate = (By.XPATH, "//a[@href='logout.asp']")
        self.target_button_ready(btn_locate).click()


class DemoOne(ButtonMixin):
    pass


class DemoTwo(LoginMixin, StockModeAMixin, LogoutMixin):
    pass


class DemoSum(DemoOne, DemoTwo):
    pass