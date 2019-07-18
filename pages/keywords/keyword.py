from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random
import time
import os
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from common.logger import logger
from common.file import mkdir

class BaseKeyword(object):
    def __init__(self,driver):
        self._driver = driver

    def open(self,url):
        self._open(url)
        logger.info("打开网址 %s"% url)

    def _open(self,url):
        self._driver.set_page_load_timeout(10)
        try:
            self._driver.get(url)
        except TimeoutException:
            logger.info("页面加载超时")
            raise Exception("页面加载超时")

    def click(self,loc,index=None):
        """
        keyword click can locate a absolutely path or a relative path with index
        :param loc:
        :param index:
        :return:
        """
        if index:
            i = int(index)
            elements = self.find_elements(loc)
            elements[i].click()
        else:
            self.find_element(loc).click()

    def double_click(self,loc):
        self._double_click(loc)

    def _double_click(self,loc):
        on_element = self.find_element(loc)
        ActionChains(self._driver).double_click(on_element).perform()

    def input_text(self,loc,text,index=None):
        """
        it can choose a absolutely location path or a relative location path
        :param loc:
        :param text:
        :param index:
        :return:
        """
        if index:
            elements = self.find_elements(loc)
            index = int(index)
            element = elements[index]
            element.clear()
            # element.send_keys(text)
            for i in range(len(text)):
                element.send_keys(text[i])
            element.send_keys(Keys.ENTER)
        else:
            element = self.find_element(loc)
            element.clear()
            element.send_keys(text)
        # comsume = time.time() - self.start
        # logger.info(comsume)
        # logger.info("输入文本 %s" % text)

    # def find_element_by_text(self,contain_text):
    #     self._find_element_by_text(contain_text)
    #
    # def _find_element_by_text(self,contain_text,timeout=10,poll_frequency=0.5):
    #     return WebDriverWait(self._driver,timeout,poll_frequency).until(EC.visibility_of_element_located((By.XPATH,".//span[contains(text(),'%s')]"%contain_text)))

    def find_element(self,loc):
        # self.start = time.time()
        element = self._find_element(loc)
        return element

    def _find_element(self,loc,timeout=10,poll_frequency=0.5):
        element = WebDriverWait(self._driver, timeout, poll_frequency).until(
            EC.visibility_of_element_located((By.XPATH, loc)))
        return element

    def find_elements(self,loc):
        elements = self._find_elements(loc)
        return elements

    def _find_elements(self,loc,timeout=10,poll_frequency=0.5):
        # return WebDriverWait(self._driver,timeout,poll_frequency).until(lambda x:x.find_elements(loc))
        return WebDriverWait(self._driver,timeout,poll_frequency).until(EC.visibility_of_all_elements_located((By.XPATH,loc)))

    def enter(self,loc):
        self._enter(loc)

    def _enter(self,loc):
        self.find_element(loc).send_keys(Keys.ENTER)

    def tab(self,loc):
        self.find_element(loc).send_keys(Keys.TAB)

    def select(self,loc,contain_text):
        self._select(loc,contain_text)

    def _select(self,loc,contain_text):
        """
        choose an option in dropdown list
        loc:the location of drop down list button
        contain_text:contains text in option location
        :param loc:
        :param contain_text:
        :return:
        """
        # self.click((loc))
        # target = WebDriverWait(self._driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH,".//span[contains(text(),'%s')]"%contain_text)))
        # auto scroll into the target
        # self._driver.execute_script("arguments[0].scrollIntoView(true);",target)
        # target.click()

        # action = ActionChains(self._driver)
        # action.move_to_element(target)
        # action.click().perform()

        self.input_text(loc,contain_text)
        # target = WebDriverWait(self._driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH,".//span[contains(text(),'%s')]"%contain_text)))
        # target.click()
        self.enter(loc)

        # self.input_text(loc,contain_text)
        # self.enter(loc)

    def rselect(self,loc1,loc2):
        self._rselect(loc1,loc2)

    def _rselect(self,loc1,loc2):
        """
        select a random option from a dropdown list
        loc1:the location of drop down list button
        loc2:all option location
        :param loc1:
        :param loc2:
        """
        self.click(loc1)
        targets = self.find_elements(loc2)
        del targets[0]
        option = random.choice(targets)
        option_text = option.text
        option.click()
        logger.info("选择选项 %s" % option_text)

    def save_screenshot(self,path):
        self._save_screenshot(path)

    def _save_screenshot(self,path):
        """
        save screenshot
        :param path: the directory of saving screenshot
        :return:
        """
        local_time = time.strftime("%Y%m%d_%H%M%S",time.localtime())
        image_name = local_time + '.png'
        image_dir = mkdir(path)
        image_path = os.path.join(image_dir,image_name)
        try:
            self._driver.get_screenshot_as_file(image_path)
            logger.info("图片 %s 已保存到路径 %s" % (image_name,image_path))
        except Exception as e:
            logger.exception("图片保存失败")
            raise e

    #get text in element
    def get_text(self, loc):
        text = self.find_element(loc).text
        return text

    # send file
    def upload_file(self, loc, file_name):
        """
        upload file
        :param loc: the path of the input tag
        :param file_name: file path
        :return: None
        """
        element = self._driver.find_element(By.XPATH,loc)
        upload_path = os.path.join(os.path.dirname(os.getcwd()),"upload",file_name)
        try:
            element.send_keys(upload_path)
        except Exception:
            logger.error("找不到文件:%s " % file_name)

    def count_elements(self,loc):
        elements = self.find_elements(loc)
        count = len(elements)
        return count

    def close(self):
        self._driver.close()

    def quit(self):
        self._driver.quit()

















