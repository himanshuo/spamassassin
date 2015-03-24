__author__ = 'himanshu'


import requests
import unittest
import json

class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/'

    def test_basic(self):
        file= open('./all_ham/X', 'rb')
        data = {}
        lineno = 0

        lines = file.readlines()

        for l in lines:
            lineno+=1
            if l=="\n" or l=="":
                break
            parts = l.split(":")
            if parts[1]:
                key = parts[0].rstrip('\n')
                key = key.lower()
                value = parts[1].rstrip('\n')
                data[key] = value

        message= '\n'.join(lines[lineno:])
        message = message.rstrip('\n')
        data['message'] = message
        data = json.dumps(data)


        headers = {
            'Content-type': 'application/json'
        }
        print data
        r = requests.post(self.url, data=data)
        self.assertEqual("HAM", r.text+"\n"+str(data))


if __name__ == '__main__':
    unittest.main()