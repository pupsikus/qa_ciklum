import unittest
# import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class StreamTVTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://streamtv.net.ua/base/')
        self.streamtv_login(login='auto', password='test')
        self.new_wrestler('SomeName', 'SomeMiddleName', 'MyLastName',
                          '01.02.1988', 'Sumska', 'Dinamo', 'FW', 'Senior',
                          '2017', 'Produced')
        self.update_wrestler(first_name='Update name')

    def update_wrestler(self, **kwargs):
        """

        Args: first_name

        """
        if 'first_name' in kwargs:
            self.update_first_name = kwargs['first_name']
        else:
            self.update_first_name = ''

    def new_wrestler(self, first_name, middle_name, last_name, birth_date,
                     dd_region, dd_fst, dd_style, dd_age, dd_year, dd_status,
                     trainer=''):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.dd_region = dd_region
        self.dd_fst = dd_fst
        self.dd_style = dd_style
        self.dd_age = dd_age
        self.dd_year = dd_year
        self.dd_status = dd_status
        self.trainer = trainer

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
        input_text.send_keys(self.last_name)
        # First Name
        input_text = self.driver.find_element_by_xpath(
            "//fg-input[@label='First name']/div/input")
        input_text.send_keys(self.first_name)
        # Middle Name
        input_text = self.driver.find_element_by_xpath(
            "//fg-input[@label='Middle name']/div/input")
        input_text.send_keys(self.middle_name)
        # Date of birth
        input_text = self.driver.find_element_by_xpath(
            "//fg-date[@label='Date of Birth']/div/input")
        input_text.send_keys(self.birth_date)
        # Trainer (not required)
        if self.trainer != '':
            pass
            # TODO select element trainer and write new trainer value
        # endregion

        # region drop-downs
        # Region select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Region']/div/select"))
        select.select_by_visible_text(self.dd_region)
        # FST select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='FST']/div/select"))
        select.select_by_visible_text(self.dd_fst)
        # Style select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Style']/div/select"))
        select.select_by_visible_text(self.dd_style)
        # Age select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Age']/div/select"))
        select.select_by_visible_text(self.dd_age)
        # Year select
        select = Select(self.driver.find_element_by_xpath(
            "//fg-select[@label='Year']/div/select"))
        select.select_by_visible_text(self.dd_year)
        # Status select
        select = Select(self.driver.find_element_by_xpath(
            "//f-select[@label='Status']/select"))
        select.select_by_visible_text(self.dd_status)
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
        if self.update_first_name != '':
            input_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, "//fg-input[@label='First name']/div/input"))
            )
            input_text.clear()
            input_text.send_keys(self.update_first_name)

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

    def streamtv_login(self, login='', password=''):
        login_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#username>div>input'))
        )
        if login == '' or password == '':
            assert 0
        login_name.send_keys(login)
        login_pass = self.driver.find_element_by_xpath(
            "//input[@type='password']")
        login_pass.send_keys(password)
        btn_submit = self.driver.find_element_by_xpath(
            "//button[@type='submit']")
        btn_submit.click()

    def tearDown(self):
        self.driver.quit()
