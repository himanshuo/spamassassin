__author__ = 'himanshu'


import requests
import unittest

class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/spam_assassin/spam_or_ham/'


    def test_basic_non_spam(self):
        files = {'file': open('sample-nonspam.txt', 'rb')}
        r = requests.post(self.url, files=files)
        self.assertEqual(u'"OK"', r.text)

    def test_almost_non_spam(self):
        files = {'file': open('sample_almost_nonspam.txt', 'rb')}
        r = requests.post(self.url, files=files)
        self.assertEqual(u'"SPAM"', r.text)

    def test_basic_spam(self):
        files = {'file': open('sample-spam.txt', 'rb')}
        r = requests.post(self.url, files=files)
        self.assertEqual(u'"SPAM"', r.text)

    def test_other_spam(self):
        files = {'file': open('sample_spam.txt', 'rb')}
        r = requests.post(self.url, files=files)
        self.assertEqual(u'"SPAM"', r.text)

if __name__ == '__main__':
    unittest.main()