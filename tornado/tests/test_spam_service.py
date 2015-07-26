__author__ = 'himanshu'


import requests
import unittest
import json
import time
import os

class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/'
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sample_input')
        self.teach_url = "http://localhost:8000/teach"

    def test_basic_non_spam(self):
        files = {'file': open(os.path.join(self.path,'sample-nonspam.txt'), 'rb')}
        data = json.dumps({
            'message': files['file'].read(),
            'email':'ho2es@virginia.edu',
        })
        r = requests.post(self.url, data=data)
        self.assertEqual("HAM", json.loads(r.text).get('decision'))
        files['file'].close()

    def test_almost_non_spam(self):
        files = {'file': open(os.path.join(self.path,'sample_almost_nonspam.txt'), 'rb')}
        data = json.dumps({
            'message': files['file'].read(),
            'email':'ho2es@virginia.edu',
        })
        r = requests.post(self.url, data=data)
        self.assertEqual("SPAM", json.loads(r.text).get('decision'))
        files['file'].close()

    def test_basic_spam(self):
        files = {'file': open(os.path.join(self.path, 'sample-spam.txt'), 'rb')}
        data = json.dumps({
            'message': files['file'].read(),
            'email':'ho2es@virginia.edu',
        })
        r = requests.post(self.url, data=data)
        self.assertEqual("SPAM", json.loads(r.text).get('decision'))
        files['file'].close()

    # def test_other_spam(self):
    #     files = {'file': open(os.path.join(self.path,'sample_long_nonspam.txt'), 'rb')}
    #     data = json.dumps({
    #         'message': files['file'].read(),
    #         'email':'ho2es@virginia.edu',
    #     })
    #     r = requests.post(self.url, data=data)
    #     self.assertEqual("HAM", json.loads(r.text).get('decision'))
    #     files['file'].close()

    def test_non_spam_with_no_email_headers(self):
        files = {'file': open(os.path.join(self.path,'non_spam_with_no_email_headers.txt'), 'rb')}
        data = json.dumps({
            'message': files['file'].read(),
            'email':'ho2es@virginia.edu',
        })
        r = requests.post(self.url, data=data)
        self.assertEqual("HAM", json.loads(r.text).get('decision'))
        files['file'].close()


    def _setup_request_data(self, filename):
        file= open(os.path.join(self.path,filename), 'rb')
        data = {}
        lineno = 0

        lines = file.readlines()

        for l in lines:
            lineno+=1
            if l=="\n" or l=="":
                break
            parts = str(l).split(':')
            if len(parts)>1:
                key = parts[0].rstrip('\n')
                key = key.lower()
                value = parts[1].rstrip('\n')
                data[key] = value

        message= '\n'.join(lines[lineno:])
        message = message.rstrip('\n')
        data['message'] = str(message) #str(message,'utf8','ignore')


        file.close()
        return data

    def test_basic(self):
        data = self._setup_request_data('1426893085.3375_3437.lorien')
        data = json.dumps(data)

        r = requests.post(self.url, data=data)
        self.assertEqual("SPAM", json.loads(r.text).get('decision'))

    def test_teach(self):
        data = self._setup_request_data('1426893085.3375_3635.lorien')
        data['is_spam']=True
        data = json.dumps(data)


        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", json.loads(r.text).get('status'))

    def test_teach_spam2(self):
        data = self._setup_request_data('1426034214.1415_367.lorien')
        data['is_spam']=True
        data = json.dumps(data)

        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", json.loads(r.text).get('status'))

    def test_teach_ham(self):
        data = self._setup_request_data('Hi')
        data['is_spam']=False
        data = json.dumps(data)

        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", json.loads(r.text).get('status'))

    def test_file(self):
        files = {'file': open(os.path.join(self.path,'1426893085.3375_3437.lorien'), 'rb')}
        r = requests.post(self.url+"?is_file=true", files=files)
        self.assertEqual(u'SPAM', json.loads(r.text).get('decision'))


    # def test_file_multiple_time(self):
    #     times=[]
    #     for t in range(0,10):
    #         files = {'file': open(self.path+'too_long.txt', 'rb')}
    #         start = time.time()
    #         r = requests.post(self.url+"?is_file=true", files=files)
    #         end =time.time()
    #         times.append(end-start)
    #         self.assertEqual(u'HAM', json.loads(r.text).get('decision'))
    #     print(times)




    def test_full_report_file(self):
        files = {'file': open(os.path.join(self.path,'1426893085.3375_3635.lorien'), 'rb')}
        r = requests.post(self.url+"?is_file=true&full_report=true", files=files)
        self.assertTrue(len(r.text)>50)
        files['file'].close()

    def test_full_report_dict(self):
        data = self._setup_request_data('1426893085.3375_3635.lorien')
        data = json.dumps(data)
        r = requests.post(self.url+"?full_report=true", data=data)
        self.assertTrue(len(r.text)>50)


    def test_incorrect_input_vals(self):
        data = self._setup_request_data('1426893085.3375_3635.lorien')
        data = json.dumps(data)
        r = requests.post(self.url+"?is_file=true", data=data)
        self.assertEqual(u"Malformed Request", r.text)




if __name__ == '__main__':
    unittest.main()