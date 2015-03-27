__author__ = 'himanshu'
import json
import requests
def _setup_request_data(filename):
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

def test(filename, full_report=False, teach=False):
    data = _setup_request_data(filename)
    if teach:
        data['is_spam']=True
    data = json.dumps(data)

    if full_report:
        r = requests.post("http://localhost:8000?full_report=true", data=data)
        print r.text
    elif teach:
        r = requests.post("http://localhost:8000/teach", data=data)
        print r.text
    else:
        r = requests.post("http://localhost:8000", data=data)
        print r.text

# test("./spam")
# test("./long_ham.txt")
# test("./spam", full_report=True)
# test("./spam", teach=True)

