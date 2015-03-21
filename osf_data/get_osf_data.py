import requests
from pprint import *
import json

response = requests.get('https://osf.io/api/v1/search/', params={
    'q': 'title:*',  # Full lucene syntax accepted: http://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    'size': 10000
})

results = response.json()
pprint(results)
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
    print project['contributors'],"has project", project['title']
    #try:
        #filename = project['title'].split()[0]
        #f= open("./ham/"+str(filename), 'w')
    #except:
        #filename = "osffile"+str(l)
        #f= open("./ham/"+str(filename), 'w')
    #f.write(project['title'].encode('UTF-8'))
    #f.close()

    # print project['title']
