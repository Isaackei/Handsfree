
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

from settings.settings import DRIVER, URL, TOTAL_NUMBER_OF_REFRESH, WEB_WAIT_TIME, PHONE_NUMBER


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
        chinese_button_locate = (By.XPATH, "/html/body/table/tbody/tr/td[2]/table/tbody/tr/td[4]/a")
        chinese_button = self.target_button_ready(locate=chinese_button_locate)
        chinese_button.click()
        self.common_refresh()


class LoginMixin(ButtonMixin):
    """针对页面登录"""
    def __init__(self):
        super().__init__()
        self.account_input_locate = "td>input"
        self.password_input_locate = "[type='password']"
        self.verify_code_locate = "//td[@class='tdc'][@valign='top']/span[%d]"
        self.verify_code_input_locate = "[name='SKey']"
        self.account_or_password_error = "//div[@class='bodydoc']/font[@color='red']/b[contains(text(),'故障')]"
        self.login_page_button_locate = "/html/body/a[4]"

    def verify_code_input(self):
        """验证码输入"""
        global num_n
        while True:
            verify_code_list = []
            compare_number = "123456"
            count_diff = 0
            for index in range(1, 7):
                try:
                    num_n = self.driver.find_element_by_xpath(self.verify_code_locate % index).text
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
                verify_code_real += self.driver.find_element_by_xpath(self.verify_code_locate % index).text
            except:
                continue
        self.driver.find_element_by_css_selector(self.verify_code_input_locate).send_keys(verify_code_real)

    def account_input(self, username=None, password=None):
        """账号密码输入"""
        self.driver.find_element_by_css_selector(self.account_input_locate).send_keys(username)
        self.driver.find_element_by_css_selector(self.password_input_locate).send_keys(password)

    def login_step(self, username=None, password=None):
        """集合登录流程"""
        self.account_input(username=username, password=password)
        self.verify_code_input()

    def login_verify(self):
        self.common_refresh()
        try:
            self.driver.find_element_by_xpath(self.account_or_password_error)
        except:
            return True
        login_locate = (By.XPATH, self.login_page_button_locate)
        login_btn = self.target_button_ready(locate=login_locate)
        login_btn.click()
        return False


class StockModeAMixin(ButtonMixin):
    """重消股"""
    def __init__(self):
        super().__init__()
        self.stock_flag = False
        self.stock_value = None
        self.r_stock_value_locate = "//input[@type='TEXT' and @name='Amount']"

    def complete_buy_load_stocks(self, locate=None, data_frame=None):
        """完成重消股购买，并记录数据"""
        self.target_button_ready(locate).click()
        data_frame.record_data()

    def stock_judge(self, locate=None):
        """判断数值是否达标"""
        self.stock_flag = False
        if float(self.stock_value) > 10:
            self.stock_flag = True
            self.target_button_ready(locate).click()

    def buy_load_stocks(self, locate=None, data_frame=None):
        """重消股初步交易操作"""
        elements = self.driver.find_element_by_xpath(self.r_stock_value_locate)
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
    def __init__(self):
        super().__init__()
        self.logout_page_button_locate = "//a[@class='GLink'][contains(text(),'退出')]"
        self.logout_conform_button_locate = "//a[@href='logout.asp']"

    def logout_account(self, data_frame=None):
        data_frame.final_record_data()
        self.target_button_ready(locate=(By.XPATH, self.logout_page_button_locate)).click()
        self.common_refresh()
        # 写死最后退出元素定位
        btn_locate = (By.XPATH, self.logout_conform_button_locate)
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
                data_frame.XJF_value = str(self.cash_point) + "F"
                data_frame.save_xjf_value()

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
        data_frame.XJF_value = str(self.cash_point_trade)
        data_frame.save_xjf_value()

    def last_check(self):
        self.common_refresh()


class PhoneNumberSetting(ButtonMixin):
    """太子支付手机号码设置"""
    def __init__(self):
        super().__init__()
        self.phone_number = PHONE_NUMBER
        self.leve_one_button_locate = "/html/body/a[10]"

    def secondary_password_verification(self):
        """判断二级密码是否正确"""
        self.common_refresh()
        error_locate = "//div[@class='bodydoc']//font[@color='red']//b[contains(text(), '故障')]"
        try:
            self.driver.find_element_by_xpath(error_locate)
        except:
            return True
        # 出现故障
        return False

    def enter_setting(self, data_frame=None):
        # ‘选项’路径
        setting_btn_locate = (By.XPATH, self.leve_one_button_locate)
        self.target_button_ready(locate=setting_btn_locate).click()
        self.common_refresh()
        # ‘账户设置路径’
        account_setting_btn_locate = (By.XPATH, "/html/body/div[1]/ul/li[1]/a")
        self.target_button_ready(locate=account_setting_btn_locate).click()
        self.common_refresh()
        # 二级密码定位
        secondary_password_locate = ("/html/body/div[1]/div[2]/form/table/tbody/tr[2]/td/input[1]")
        self.driver.find_element_by_xpath(secondary_password_locate).send_keys(data_frame.user_account[2])
        # ‘下一步’按钮定位
        next_btn_locate = (By.XPATH, "/html/body/div[1]/div[2]/form/table/tbody/tr[2]/td/input[2]")
        self.target_button_ready(locate=next_btn_locate).click()
        self.common_refresh()
        check_point = self.secondary_password_verification()
        return check_point

    def get_phone_number(self, data_frame=None):
        """查找太子支付手机号码"""
        # 太子支付手机号码定位
        phone_number_locate = "//td[@class='tdc']//input[@type='TEXT' and @name='TZN']"
        phone_number_value = self.driver.find_element_by_xpath(phone_number_locate).get_attribute("value")
        if phone_number_value == "":  # 没有设置支付号码
            self.driver.find_element_by_xpath(phone_number_locate).send_keys(self.phone_number)
            # 提交按钮
            submit_btn_locate = (By.XPATH, "/html/body/div[1]/table/tbody/tr[30]/td/input[2]")
            self.target_button_ready(locate=submit_btn_locate).click()
            self.common_refresh()
            data_frame.save_phone_number(phone_num=self.phone_number)
        else:  # 已设置了支付号码，执行记录
            data_frame.save_phone_number(phone_num=phone_number_value)


class ForcePhoneNumberSetting(ButtonMixin):
    """强制设置太子支付手机号码设置"""
    def __init__(self):
        super().__init__()
        self.phone_number = PHONE_NUMBER

    def f_secondary_password_verification(self):
        """判断二级密码是否正确"""
        self.common_refresh()
        error_locate = "//div[@class='bodydoc']//font[@color='red']//b[contains(text(), '故障')]"
        try:
            self.driver.find_element_by_xpath(error_locate)
        except:
            return True
        # 出现故障
        return False

    def f_enter_setting(self, data_frame=None):
        # ‘选项’路径
        setting_btn_locate = (By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[19]/a")
        self.target_button_ready(locate=setting_btn_locate).click()
        self.common_refresh()
        # ‘账户设置路径’
        account_setting_btn_locate = (By.XPATH, "/html/body/div[1]/ul/li[1]/a")
        self.target_button_ready(locate=account_setting_btn_locate).click()
        self.common_refresh()
        # 二级密码定位
        secondary_password_locate = ("/html/body/div[1]/div[2]/form/table/tbody/tr[2]/td/input[1]")
        self.driver.find_element_by_xpath(secondary_password_locate).send_keys(data_frame.user_account[2])
        # ‘下一步’按钮定位
        next_btn_locate = (By.XPATH, "/html/body/div[1]/div[2]/form/table/tbody/tr[2]/td/input[2]")
        self.target_button_ready(locate=next_btn_locate).click()
        self.common_refresh()
        check_point = self.f_secondary_password_verification()
        return check_point

    def f_get_phone_number(self, data_frame=None):
        """查找太子支付手机号码"""
        # 太子支付手机号码定位
        phone_number_locate = "//td[@class='tdc']//input[@type='TEXT' and @name='TZN']"
        phone_number_value = self.driver.find_element_by_xpath(phone_number_locate).get_attribute("value")
        if phone_number_value != self.phone_number:
            # 清除输入框内的内容
            self.driver.find_element_by_xpath(phone_number_locate).clear()
            self.driver.find_element_by_xpath(phone_number_locate).send_keys(self.phone_number)
            # 提交按钮
            submit_btn_locate = (By.XPATH, "/html/body/div[1]/table/tbody/tr[30]/td/input[2]")
            self.target_button_ready(locate=submit_btn_locate).click()
            self.common_refresh()
            data_frame.save_phone_number(phone_num=self.phone_number)
        else:  # 已设置了支付号码，执行记录
            data_frame.save_phone_number(phone_num=phone_number_value)


class WindrowCashToTaiZhi(ButtonMixin):
    """奖金分转太子提现"""
    def __init__(self):
        super().__init__()
        self.level_one_page_button_locate = "/html/body/a[10]"
        self.cash_point = None
        self.cash_point_trade = None
        self.cash_point_value_locate = "/html/body/div[1]/table/tbody/tr[2]/td[3]"
        self.entry_cash_point_transfer_button_locate = "/html/body/div[1]/table/tbody/tr[2]/td[2]/a"
        self.taizhi_transfer_button_locate = "/html/body/div[1]/ul/li[5]/a"
        self.taizhi_account_locate = "//td[@class='tdd' and @valign='top']"
        self.taizhi_account = None
        self.value_input_locate = "/html/body/div[1]/table/tbody/tr[7]/td/input"
        self.second_password_locate = "/html/body/div[1]/table/tbody/tr[8]/td/input"
        self.error_trade_value = "//div[@class='bodydoc']//font[@color='red']//b[contains(text(), '故障')]"
        self.next_step_locate = "/html/body/div[1]/table/tbody/tr[9]/td/input[2]"
        self.complete_trade_button_locate = "//*[@id='Submit']/input[2]"

    def first_error_judge(self):
        self.common_refresh()
        try:
            self.driver.find_element_by_xpath(self.error_trade_value)
        except:
            return False
        return True

    def value_input(self, data_frame=None):
        self.cash_point_trade = str(int((self.cash_point - 10) / 1.05))
        self.driver.find_element_by_xpath(self.value_input_locate).send_keys(self.cash_point_trade)
        self.driver.find_element_by_xpath(self.second_password_locate).send_keys(data_frame.user_account[2])

    def value_string_transfer(self, num=None):
        if num == "-":
            self.cash_point = 0
        self.cash_point = float(num.replace(",", ""))

    def cash_point_to_taizhi(self, data_frame=None):
        self.entry_first_page_from_home(locate=(By.XPATH, self.level_one_page_button_locate))
        try:
            temp_num = self.driver.find_element_by_xpath(self.cash_point_value_locate).text
            print(temp_num, data_frame.user_account[0])
            self.value_string_transfer(num=temp_num)
        except:
            self.cash_point = 0
        finally:
            if self.cash_point > 115:
                # 进入奖金分提现
                self.target_button_ready(locate=(By.XPATH, self.entry_cash_point_transfer_button_locate)).click()
                self.target_button_ready(locate=(By.XPATH, self.taizhi_transfer_button_locate)).click()
                self.taizhi_account = self.driver.find_element_by_xpath(self.taizhi_account_locate).text
                data_frame.save_phone_number(phone_num=self.taizhi_account)
                self.value_input(data_frame=data_frame)
                self.target_button_ready(locate=(By.XPATH, self.next_step_locate)).click()
                check_point_first = self.first_error_judge()
                if check_point_first:
                    data_frame.XJF_value = "F"
                    data_frame.save_xjf_value()
                    return None
                self.target_button_ready(locate=(By.XPATH, self.complete_trade_button_locate)).click()
                data_frame.XJF_value = self.cash_point_trade
                data_frame.save_xjf_value()
                return None
            else:
                data_frame.XJF_value = str(self.cash_point) + "F"
                data_frame.save_xjf_value()
                return None


class InformationRecord(ButtonMixin):
    """记录注册时间及回本股份信息"""
    def __init__(self):
        super().__init__()
        self.level_one_page_button_locate_1 = "//a[@class='GLink' and @href='setting.asp']"
        self.my_account_button_locate = "/html/body/div[1]/ul/li[1]/a"
        self.my_account_information_locate = "/html/body/div[1]/table/tbody/tr[4]/td"
        self.account_register_time = None
        self.wallet_button_locate_1 = "/html/body/a[11]"
        self.information_check_point = "//*[text()='配套股收益']/../following-sibling::td"  # 完全查找文字，部分为[contains(text(),"xxx")]
        self.information_data_locate = "/html/body/div[1]/table/tbody/tr[15]/td[3]"
        self.information_data = None

    def register_time(self, data_frame=None):
        self.entry_first_page_from_home(locate=(By.XPATH, self.level_one_page_button_locate_1))
        self.entry_first_page_from_home(locate=(By.XPATH, self.my_account_button_locate))
        self.common_refresh()
        self.account_register_time = self.driver.find_element_by_xpath(self.my_account_information_locate).text
        self.entry_first_page_from_home(locate=(By.XPATH, self.wallet_button_locate_1))
        self.common_refresh()
        # 判断该账号是否出现需要信息
        try:
            self.information_data = self.driver.find_element_by_xpath(self.information_check_point).text
        except:
            self.information_data = "-"
        print(self.information_data)
        data_frame.save_phone_number(phone_num=self.account_register_time)
        data_frame.save_information_data(info_data=self.information_data)


class DemoOne(ButtonMixin):
    pass


class DemoTwo(LoginMixin,
              StockModeAMixin,
              LogoutMixin,
              CashPointMixin,
              PhoneNumberSetting,
              ForcePhoneNumberSetting,
              WindrowCashToTaiZhi,
              InformationRecord):
    pass


class DemoSum(DemoOne, DemoTwo):
    pass