from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retreve_it_later(self):
        # Fizzywig, The Powerful Wizard, has heard of a new online to-do app that will
        # help him keep track of his worlds, he goes to the homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Align the conjunction of the spheres', [row.text for row in rows])

        # There is still a text box inviting him to add another item he enters
        # "Prepare the Ochre for the ritual of invocation"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Prepare the Ochre for the ritual of invocation')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        # The page updates again and the first two tasks appear on his list.

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Align the conjunction of the spheres', [row.text for row in rows])
        self.assertIn('2: Prepare the Ochre for the ritual of invocation', [row.text for row in rows])
        # Worried about this arcane formula being destroyed into the ether, Fizzywig
        # is releved to find the site has created a unique URL for him (explanitory
        # text to this effect is what catches his eye)
        self.fail('Finish the Test')

        # he visits the URL his to-do list is still there

        # Satisfied, he returns to his slumbatorium

if __name__ == '__main__':
    unittest.main(warnings='ignore')
