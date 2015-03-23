import requests
from pprint import *
import json

response = requests.get('https://osf.io/api/v1/search/', params={
    'q': 'title:*',  # Full lucene syntax accepted: http://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    'size': 10000
})

results = response.json()
#pprint(results)
#
# data = json.dumps({
#     'query': {
#         'category:project': {}  # Accepts the full elasticsearch DSL: http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
#     }
# })
# headers = {
#     'Content-type': 'application/json'
# }
# response = requests.post('https://osf.io/api/v1/search/', data=data, headers=headers)
#
# results = response.json()
# pprint(results)
print("---------")

l=0
for project in results['results']:
    #print project['contributors'],"has project", project['title']
    try:
        filename = project['title'].split()[0]
        f= open("./ham/"+str(filename), 'w')
    except:
        filename = "osffile"+str(l)
        f= open("./ham/"+str(filename), 'w')
    try:
        fields = ['title','description', 'contributors', 'tags']
        out=""
        for f in fields:
            value = project.get(f,'') or ""
            value = str(value.encode('utf-8','ignore'))
            text = f.capitalize() +": " + value+"\n"
            text = text.encode('utf-8','ignore')
            out+=text
        out+="\n"
        for f in ['title','description']:
            value = project.get(f,'') or ""
            value = str(value.encode('utf-8','ignore'))
            text = f.capitalize() +": " + value+"\n"
            text = text.encode('utf-8','ignore')
            out+=text
        f.write(out)
        f.close()
    except Exception as e:
        print(e)

