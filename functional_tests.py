from selenium import webdriver
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
        self.fail('Finish the test!')

        #He is invited to enter a to-do list item staright away

        #he types "Align the conjuntion of the spheres" into a text-box

        # When he hits enter the page updates and now has 1: Align the conjuntion of
        # spheres" as an item in the to-do lists

        # There is still a text box inviting him to add another item he enters
        # "Prepare the Ochre for the ritual of invocation"

        # The page updates again and the first two tasks appear on his list.

        # Worried about this arcane formula being destroyed into the ether, Fizzywig
        # is releved to find the site has created a unique URL for him (explanitory
        # text to this effect is what catches his eye)


        # he visits the URL his to-do list is still there

        # Satisfied, he returns to his slumbatorium

if __name__ == '__main__':
    unittest.main(warnings='ignore')
