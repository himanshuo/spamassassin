__author__ = 'himanshu'
import os
import subprocess
import requests
from pprint import *
import json
import shlex

def remove_unneccessary_headers_from_spam_emails(folder_name):
    """
    remove headers that are unneccessary from spam email headers
    """
    files_folders = os.listdir(folder_name)
    i=0
    for f in files_folders:
        try:
            if f[0:3] == "dir" or f[0:3]=="spa":
                remove_unneccessary_headers_from_spam_emails(folder_name.rstrip("/")+"/"+f)
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



def get_osf_data_from_elastic_search(show_data=False):
    response = requests.get('https://osf.io/api/v1/search/', params={
        'q': 'title:*',  # Full lucene syntax accepted: http://lucene.apache.org/core/2_9_4/queryparsersyntax.html
        'size': 10000
    })

    results = response.json()
    if show_data:
        pprint(results)
        print("---------")
    return results

def convert_osf_elastic_data_to_email_format(results):
    l=0
    for project in results['results']:
        l+=1
        #print project['contributors'],"has project", project['title']
        try:
            filename = project['title'].split()[0]
            f= open("./osf_data/"+str(filename), 'w')
        except:
            filename = "osffile"+str(l)
            f= open("./osf_data/"+str(filename), 'w')
        try:

            fields = ['title','description', 'contributors', 'tags']
            out=u""
            for field in fields:
                value = project.get(field,'') or u""
                if (isinstance(value, list)):
                    value =  u', '.join(value)
                #value = value.encode('utf-8','ignore')
                text = field.capitalize() +u": " + value+u"\n"
                #text = text.encode('utf-8','ignore')
                out+=text
            out+="\n"
            #out=out.encode('utf-8','ignore')
            for field in ['title','description']:
                value = project.get(field,'') or u""
                value += u"\n"
                out += value
            f.write(out.encode('utf-8','ignore'))
            f.close()
        except Exception as e:
            print(e)
            import pdb;pdb.set_trace()




def utility_for_osf_spam_or_ham(folder_name):
    """
    commandline utility for determining whether osf info is spam or ham and then moving to correct file.
    """
    files_folders = os.listdir(folder_name)
    for f in files_folders:
        try:
            if f[0:3] == "dir":
                pass
            else:
                cur_file_path = folder_name.rstrip("/")+"/"+f

                cur_file_contents = open(cur_file_path,'r').read()
                print cur_file_contents
                decision = input("spam or ham (enter 's' or 'h' or '<enter>'):")
                if decision == 's':
                    from_folder = "./osf_data/"+f
                    to_folder = "./osf_data/osf_spam/"+f
                    command = "mv "+from_folder + " "+ to_folder
                    args = shlex.split(command)
                    subprocess.call(args)
                elif decision == 'h':
                    from_folder = "./osf_data/"+f
                    to_folder = "./osf_data/osf_ham/"+f
                    command = "mv "+from_folder + " "+ to_folder
                    args = shlex.split(command)
                    subprocess.call(args)

        except:
            print f