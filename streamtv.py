import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class StreamTVTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://streamtv.net.ua/base/')
        self.streamtv_login()

    def test_create(self):
        """
        Create new wrestler, save it and close it.

        If you read comments(at least the first one) then you notice a bug
        description:  'Status' dropdown has not required option fot select
        when create new member, but on update the 'Status' field is required.
        """
        # New button click
        btn_new = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                ".form-group>button[type='button']"))
        )
        btn_new.click()

        # region text inputs
        # Last Name
        input_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//fg-input[@label='Last name']/div/input"))
        )
        input_text.send_keys('MyLastName')
        # First Name
        input_text = self.driver.find_element_by_xpath(
            "//fg-input[@label='First name']/div/input")
        input_text.send_keys('SomeName')
        # Middle Name
        input_text = self.driver.find_element_by_xpath(
            "//fg-input[@label='Middle name']/div/input")
        input_text.send_keys('SomeMiddleName')
        # Date of birth
        input_text = self.driver.find_element_by_xpath(
            "//fg-date[@label='Date of Birth']/div/input")
        input_text.send_keys('01.02.1988')
        # endregion

        # region drop-downs
        # Region select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Region']/div/select"))
        select.select_by_visible_text('Sumska')
        # FST select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='FST']/div/select"))
        select.select_by_visible_text('Dinamo')
        # Style select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Style']/div/select"))
        select.select_by_visible_text('FW')
        # Age select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Age']/div/select"))
        select.select_by_visible_text('Senior')
        # Year select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Year']/div/select"))
        select.select_by_visible_text('2017')
        # Status select
        select = Select(self.driver.find_element_by_xpath(
            "//f-select[@label='Status']/select"))
        select.select_by_visible_text('Produced')
        # endregion

        # Button save
        btn_save = self.driver.find_element_by_css_selector(
            'button.btn-success')
        t1 = datetime.now()
        while not btn_save.is_enabled():
            t2 = datetime.now()
            delta = (t2 - t1)
            # wait for 2 seconds
            if delta.seconds > 2:
                break
        btn_save.click()

        # Button close
        btn_close = self.driver.find_element_by_css_selector(
            'li.active>a>tab-heading>div>div>ico')
        t1 = datetime.now()
        while not btn_close.is_displayed():
            t2 = datetime.now()
            delta = (t2 - t1)
            # wait for 2 seconds
            if delta.seconds > 2:
                break
        btn_close.click()

    def test_update(self):
        """
        Update one input value (Name) with new value
        """
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//table/tbody"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        rows[0].click()
        input_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//fg-input[@label='First name']/div/input"))
        )
        input_text.clear()
        input_text.send_keys('Update Name')
        # Button save
        btn_save = self.driver.find_element_by_css_selector(
            'button.btn-success')
        t1 = datetime.now()
        while not btn_save.is_enabled():
            t2 = datetime.now()
            delta = (t2 - t1)
            # wait for 2 seconds
            if delta.seconds > 2:
                break
        btn_save.click()

    def test_delete(self):
        """
        Delete 2 first rows
        """
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//table/tbody"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        index = 0
        for row in rows:
            index = index + 1
            if index == 3:
                break
            t1 = datetime.now()
            while not row.is_displayed():
                t2 = datetime.now()
                delta = (t2 - t1)
                # wait for 2 seconds
                if delta.seconds > 2:
                    break
            row.click()
            btn_delete = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'wrestler')]"
                    "//div//div[2]//button"))
            )
            t1 = datetime.now()
            while not btn_delete.is_displayed():
                t2 = datetime.now()
                delta = (t2 - t1)
                # wait for 2 seconds
                if delta.seconds > 2:
                    break
            btn_delete.click()
            btn_ok = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class,'modal-content')]"
                    "//div[contains(@class,'modal-footer')]"
                    "//button[contains(@class,'btn-success')]"))
            )
            btn_ok.click()

    def test_read(self):
        """
        Read one input element and one select element.
        Print result
        """
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//table/tbody"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        rows[0].click()
        # Read name
        input_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//fg-input[@label='First name']/div/input"))
        )
        text = input_text.get_attribute('value')
        # Read FST
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='FST']/div/select"))
        text2 = select.first_selected_option.text
        print('Name - ' + text, ' FST - ' + text2)

        # Button close
        btn_close = self.driver.find_element_by_css_selector(
            'li.active>a>tab-heading>div>div>ico')
        t1 = datetime.now()
        while not btn_close.is_displayed():
            t2 = datetime.now()
            delta = (t2 - t1)
            # wait for 2 seconds
            if delta.seconds > 2:
                break
        btn_close.click()

    def streamtv_login(self):
        login_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#username>div>input'))
        )
        login_name.send_keys('auto')
        login_pass = self.driver.find_element_by_xpath(
            "//input[@type='password']")
        login_pass.send_keys('test')
        btn_submit = self.driver.find_element_by_xpath(
            "//button[@type='submit']")
        btn_submit.click()

    def tearDown(self):
        self.driver.quit()
