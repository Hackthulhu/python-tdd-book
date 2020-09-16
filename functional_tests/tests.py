from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        #Fizzywig goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 728)

        #He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] +
            inputbox.size['width']/2,
            512,
            delta = 10
            )
        #after starting a new list he sees the input box remains centered
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] +
            inputbox.size['width']/2,
            512,
            delta = 10
            )

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Fizzywig, The Powerful Wizard, has heard of a new online to-do app that will
        # help him keep track of his worlds, he goes to the homepage
        self.browser.get(self.live_server_url)

        #he notives the page titl and header mention to-do lists
        self.assertIn('To-Do',  self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        #He is invited to enter a to-do list item staright away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        #he types "Align the conjuntion of the spheres" into a text-box
        inputbox.send_keys('Align the conjunction of the spheres')


        # When he hits enter the page updates and now has 1: Align the conjuntion of
        # spheres" as an item in the to-do lists
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Align the conjunction of the spheres')

        # There is still a text box inviting him to add another item he enters
        # "Prepare the Ochre for the ritual of invocation"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Prepare the Ochre for the ritual of invocation')
        inputbox.send_keys(Keys.ENTER)


        # The page updates again and the first two tasks appear on his list.

        self.wait_for_row_in_list_table('1: Align the conjunction of the spheres')
        self.wait_for_row_in_list_table('2: Prepare the Ochre for the ritual of invocation')
        # Worried about this arcane formula being destroyed into the ether, Fizzywig
        # is releved to find the site has created a unique URL for him (explanitory
        # text to this effect is what catches his eye)


        # he visits the URL his to-do list is still there

        # Satisfied, he returns to his slumbatorium

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Fizzywig starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Align the conjunction of the spheres')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Align the conjunction of the spheres')
        # He notices his arcane forumula has a unique RUL
        fizzywig_list_url = self.browser.current_url
        self.assertRegex(fizzywig_list_url, '/lists/.+')

        # Now Supercow, a new user comes onto the scene
        ## she uses a new browser to ensure that she is sharing none of fizzywigs
        ## arcane foruma are shared with Supercow

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Supercow visits the homepage, there is no evidence of Fizzywigs list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Align the conjunction of the spheres', page_text)
        self.assertNotIn('Prepare the Ochre for the ritual of invocation', page_text)

        # SuperCow starts a new list of what she needs to do to save the town of
        # Cheesetopia from the evil doctor tofu

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Clear tofu\'s goons from the creamery')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Clear tofu\'s goons from the creamery')

        #SuperCow gets her own unique URL

        supercow_list_url = self.browser.current_url
        self.assertRegex(supercow_list_url, '/lists/.+')
        self.assertNotEqual(fizzywig_list_url, supercow_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Align the conjunction of the spheres', page_text)
        self.assertIn('Clear tofu\'s goons from the creamery', page_text)
