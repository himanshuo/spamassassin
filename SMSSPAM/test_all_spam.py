__author__ = 'himanshu'


import requests
import unittest
import os
class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/'


    def test_spam(self):

        for files in os.walk('./spam/'):

            for f in files[2]:


                content = open("./spam/"+f, 'rb').read()
                r = requests.post(self.url, data=content)
                self.assertEqual("SPAM", r.text)

    # def test_ham(self):
    #     files = {'file': open('sample_almost_nonspam.txt', 'rb')}
    #     r = requests.post(self.url, data=files['file'].read())
    #     self.assertEqual("SPAM", r.text)


    


if __name__ == '__main__':
    unittest.main()