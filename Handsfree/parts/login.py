from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parts import setting


def get_url_page(driver):
    """前往地址"""
    target_url = setting.TARGET_URL
    driver.get(target_url)
    return driver


def web_ready(driver=None):
    """判断登录页面加载情况"""
    refresh_count = 0
    while refresh_count < setting.NUMBER_OF_REFRESH:
        try:
            button_element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@class='button'][@type='SUBMIT']")))
            return button_element
        except:
            driver.refresh()
            refresh_count += 1
    return False


def user_input(driver=None, username=None, password=None):
    """账号密码输入"""
    driver.find_element_by_css_selector("td>input").send_keys(username)
    driver.find_element_by_css_selector("[type='password']").send_keys(password)


def verify_code_input(driver=None):
    """验证码输入"""
    while True:
        verify_code_list = []
        compare_number = "123456"
        count_diff = 0
        for index in range(1, 7):
            num_n = driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
            verify_code_list.append(num_n)
            if num_n != compare_number[index - 1]:
                count_diff += 1

        if count_diff > 0:
            break

    verify_code_real = ""
    for index in range(1, 7):
        verify_code_real += driver.find_element_by_xpath("//td[@class='tdc']/span[%d]" % index).text
    driver.find_element_by_css_selector("[name='SKey']").send_keys(verify_code_real)


# def web_load():
#     """主启动"""
#     driver = start_project()
#
#     elements = web_ready(driver=driver)
#     if elements is False:
#         print("F")
#     else:
#         user_input(driver=driver)
#         verify_code_input(driver=driver)
#         elements.click()
