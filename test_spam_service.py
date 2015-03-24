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
        data['message'] = message
        return data

    def test_basic(self):
        data = self._setup_request_data('./all_spam/1426089335.3311_583.lorien')
        data = json.dumps(data)


        headers = {
            'Content-type': 'application/json'
        }

        r = requests.post(self.url, data=data)
        self.assertEqual("HAM", r.text)

    def test_teach(self):
        data = self._setup_request_data('./all_spam/1426089335.3311_583.lorien')
        data = json.dumps(data)


        headers = {
            'Content-type': 'application/json'
        }

        r = requests.post(self.teach_url, data=data)
        self.assertEqual("Learned.", r.text)



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
                    if "Received:" not in cur_file_contents[lineno] and "Delivered-To:" not in cur_file_contents[lineno] :
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