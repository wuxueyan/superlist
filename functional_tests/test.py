from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.support.wait import	WebDriverWait
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys

class NewVisitorTest(StaticLiveServerTestCase):
	# 类专属方法，可通过类名进行调用
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.sqlit('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3000)

	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self,row_text):
		rows = self.browser.find_elements_by_css_selector('#id_list_table tr')
		self.assertIn(row_text,[row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.server_url)
		self.assertIn('To-Do',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)

		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(2)
		edith_list_url = self.browser.current_url

		self.assertRegex(edith_list_url,'/lists/.+')
		self.browser.implicitly_wait(10)
		time.sleep(2)
		self.check_for_row_in_list_table('1:Buy peacock feathers')
		self.browser.implicitly_wait(10)
		time.sleep(2)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		time.sleep(2)
		inputbox.send_keys(Keys.ENTER)
		time.sleep(2)
		self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
		self.check_for_row_in_list_table('1:Buy peacock feathers')

		
		self.browser.quit()
		self.browser = webdriver.Firefox()

		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertNotIn('make a fly',page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		edith_list_url = self.browser.current_url
		inputbox.send_keys(Keys.ENTER)
		time.sleep(2)
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url,'/lists/.+')
		self.assertNotEqual(francis_list_url,edith_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Buy peacock feathers',page_text)
		self.assertIn('Buy milk',page_text)
		time.sleep(2)
		#self.fail("Finish the test!")
	
	def test_layout_and_styling(self):
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x']+inputbox.location['y'] / 2,
			512,delta = 5
		)
		
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x']+inputbox.location['y'] / 2,
			512,
			delta=5
		)

