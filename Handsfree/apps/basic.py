import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

from settings.settings import DRIVER, URL, TOTAL_NUMBER_OF_REFRESH, WEB_WAIT_TIME


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
            WebDriverWait(self.driver, 15).until(
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
                print("page load fail common_refresh")
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
            try:
                button = WebDriverWait(self.driver, WEB_WAIT_TIME).until(EC.element_to_be_clickable(locate))
                if button:

                    return button
            except:
                self.driver.refresh()
                refresh_count += 1

    def entry_first_page_from_home(self, locate=None):
        """从主页前往第一层页面"""
        self.target_button_ready(locate=locate).click()

    def chinese_login_page_start(self):
        self.get_url()
        chinese_button_locate = (By.XPATH, "/html/body/table/tbody/tr[1]/td/span[2]/a")
        chinese_button = self.target_button_ready(locate=chinese_button_locate)
        chinese_button.click()
        self.common_refresh()


class LoginMixin(ButtonMixin):
    """针对页面登录"""

    def verify_code_input(self):
        """验证码输入"""

        global num_n
        while True:
            verify_code_list = []
            compare_number = "123456"
            count_diff = 0
            for index in range(1, 7):
                # num_n = self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
                try:
                    num_n = self.driver.find_element_by_xpath("//td[@class='tdc'][@valign='top']/span[%d]" % index).text
                    verify_code_list.append(num_n)
                except:
                    continue
                if num_n != compare_number[index - 1]:
                    count_diff += 1

            if count_diff > 0:
                break
        # 第二次获取验证码，预防延迟
        global verify_code_real
        verify_code_real = ""
        for index in range(1, 7):
            try:
                verify_code_real += self.driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
            except:
                continue
        self.driver.find_element_by_css_selector("[name='SKey']").send_keys(verify_code_real)

    def account_input(self, username=None, password=None):
        """账号密码输入"""
        self.driver.find_element_by_css_selector("td>input").send_keys(username)
        self.driver.find_element_by_css_selector("[type='password']").send_keys(password)

    def login_step(self, username=None, password=None):
        """集合登录流程"""
        self.account_input(username=username, password=password)
        self.verify_code_input()

    def login_verify(self):
        self.common_refresh()
        error_locate = ("//div[@class='bodydoc']/font[@color='red']/b[contains(text(),'故障')]")
        try:
            self.driver.find_element_by_xpath(error_locate)
        except:
            return True
        login_locate = (By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[7]/a")
        login_btn = self.target_button_ready(locate=login_locate)
        login_btn.click()
        return False


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


class CashPointMixin(ButtonMixin):
    """现金分"""
    def __init__(self):
        super().__init__()
        self.cash_point = None
        self.cash_point_trade = None
        self.cash_point_flag = False

    def cash_point_judge(self, locate=None, data_frame=None):
        """奖金分转现金分，流程前判断，并进入输入界面"""
        try:
            temp_num = self.driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr[2]/td[3]").text
            print(temp_num, data_frame.user_account[0])
            self.cash_point = float(temp_num)
        except:
            print("没获取到数据")
            self.cash_point = 0
        finally:
            self.cash_point_flag = False
            if self.cash_point > 21.5:
                self.cash_point_flag = True
                target_btn = (By.XPATH, "/html/body/div[1]/table/tbody/tr[2]/td[2]/a")
                self.target_button_ready(locate=target_btn).click()
                self.cash_point_trade = str(int((self.cash_point - 10)/1.15))
                self.common_refresh()
                self.target_button_ready(locate=locate).click()
            else:
                data_frame.stock_R_pin = str(self.cash_point)
                data_frame.record_data()

    def cash_point_process(self, data_frame=None, locate=None):
        self.common_refresh()
        value_input_locate = ("/html/body/div[1]/table/tbody/tr[6]/td/input")
        print("输入数字")
        self.driver.find_element_by_xpath(value_input_locate).send_keys(self.cash_point_trade)
        password2_input_locate = ("/html/body/div[1]/table/tbody/tr[7]/td/input")
        print("输入密码")
        self.driver.find_element_by_xpath(password2_input_locate).send_keys(data_frame.user_account[2])
        self.target_button_ready(locate=locate).click()

    def cash_point_trade_finish(self, locate=None, data_frame=None):
        self.common_refresh()
        self.target_button_ready(locate=locate).click()
        data_frame.stock_R_pin = str(self.cash_point_trade)
        data_frame.record_data()

    def last_check(self):
        self.common_refresh()


class DemoOne(ButtonMixin):
    pass


class DemoTwo(LoginMixin, StockModeAMixin, LogoutMixin, CashPointMixin):
    pass


class DemoSum(DemoOne, DemoTwo):
    pass