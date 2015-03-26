__author__ = 'himanshu'


import requests
import unittest
import json
import os
class TestSpamService(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/'
        self.teach_url = "http://localhost:8000/teach"



    def _setup_request_data(self, filename):
        file= open(filename, 'rb')
        data = {}
        lineno = 0

        lines = file.readlines()

        for l in lines:
            lineno+=1
            if l=="\n" or l=="":
                break
            parts = l.split(":")
            if len(parts)>1:
                key = parts[0].rstrip('\n')
                key = key.lower()
                value = parts[1].rstrip('\n')
                data[key] = value

        message= '\n'.join(lines[lineno:])
        message = message.rstrip('\n')
        data['message'] = unicode(message,'utf8','ignore')
        file.close()
        return data

    def test_basic(self):
        data = self._setup_request_data('./all_spam/dir_114/1426893085.3375_3635.lorien')
        data = json.dumps(data)

        r = requests.post(self.url, data=data)
        self.assertEqual("SPAM", r.text)

    def test_teach(self):
        data = self._setup_request_data('./all_spam/dir_114/1426893085.3375_3635.lorien')
        data['is_spam']=True
        data = json.dumps(data)


        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", r.text)

    def test_teach_spam2(self):
        data = self._setup_request_data('./all_spam/dir_001/1426034214.1415_367.lorien')
        data['is_spam']=True
        data = json.dumps(data)

        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", r.text)

    def test_teach_ham(self):
        data = self._setup_request_data('./all_ham/Hi')
        data['is_spam']=False
        data = json.dumps(data)

        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned", r.text)

    def test_file(self):
        files = {'file': open('./all_spam/dir_114/1426893085.3375_3635.lorien', 'rb')}
        r = requests.post(self.url+"?is_file=true", files=files)
        self.assertEqual(u'SPAM', r.text)

    def test_full_report_file(self):
        files = {'file': open('./all_spam/dir_114/1426893085.3375_3635.lorien', 'rb')}
        r = requests.post(self.url+"?is_file=true&full_report=true", files=files)
        self.assertTrue(r.text)

    def test_full_report_dict(self):
        data = self._setup_request_data('./all_spam/dir_114/1426893085.3375_3635.lorien')
        data = json.dumps(data)
        r = requests.post(self.url+"?full_report=true", data=data)
        self.assertTrue(len(r.text)>50)

    def test_incorrect_input_vals(self):
        data = self._setup_request_data('./all_spam/dir_114/1426893085.3375_3635.lorien')
        data = json.dumps(data)
        r = requests.post(self.url+"?is_file=true", data=data)
        self.assertEqual(u"Malformed Request", r.text)

    def test_num_correct_osf_ham(self):
        files_folders = os.listdir("./all_ham/")
        osf_files = []
        for f in files_folders:
            if not f[0].isdigit() and not f[0:3]=="dir":
                osf_files.append(f)
        correct = 0
        for f in osf_files:
            data = self._setup_request_data('./all_ham/'+f)
            data = json.dumps(data)
            r = requests.post(self.url, data=data)
            if r.text == u"HAM":
                correct+=1
            else:
                print r.text
        self.assertEqual(len(osf_files),correct)


        #r = requests.post(self.teach_url, data=data)
        #self.assertEqual("Learned", r.text)



def fix_messages(folder_name):
    files_folders = os.listdir(folder_name)
    i=0
    for f in files_folders:
        try:
            if f[0:3] == "dir" or f[0:3]=="spa":
                fix_messages(folder_name.rstrip("/")+"/"+f)
            else:
                cur_file_path = folder_name.rstrip("/")+"/"+f
                cur_file_contents = open(cur_file_path,'r').readlines()
                cur_file = open(cur_file_path,'w')
                i+=1
                for lineno in range(0,len(cur_file_contents)-1):
                    #cur_file.write(cur_file_contents[lineno])
                    if "Received:" not in cur_file_contents[lineno] and "Delivered-To:" not in cur_file_contents[lineno] \
                            and " by " not in cur_file_contents[lineno] and "  with " not in cur_file_contents[lineno]:
                        cur_file.write(cur_file_contents[lineno])
                        #print "YES", cur_file_contents[lineno]
                    else:
                        pass
                        #print "NO", cur_file_contents[lineno]
                cur_file.close()
        except:
            print f






if __name__ == '__main__':
    unittest.main()
    #fix_messages("./all_spam/")