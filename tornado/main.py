

import tornado.ioloop
import tornado.web
from tornado import gen, httpclient
import os

#for calling spamc
import subprocess
import shlex
from concurrent.futures import ThreadPoolExecutor

#trying to do async
import asyncio
import requests
from tornado.process import *
"""
import asyncio
import requests

@asyncio.coroutine
def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
    response1 = yield from future1
    response2 = yield from future2
    print(response1.text)
    print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""

#parallel
thread_pool = ThreadPoolExecutor(4)#number is max number of parallel threads. why not more?

class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        #setup command
        command = "spamc -c"
        args = shlex.split(command)

        #send command and get result
        self.proc = tornado.process.Subprocess(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)




    def slow_method(self, data):
        arr = []
        for i in range(1,100):
            arr[0] = len(str(httpclient.AsyncHTTPClient.fetch("http://www.google.co.uk")))
        self.finish()


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        #############POST data ##########################
        try:
            print("----------start------------------")
            #get data
            data = self.request.body
            #todo: extract email from body.

            #print(data)
            """
            #probably best to go through various ways of input in a method and use whichever one works.
            data = self.get_body_arguments('email','')
            print(data)
            data = self.get_arguments('email','')
            print(data)
            """

            #result = self.proc.communicate(data)

            #self.proc.communicate

            result = yield from thread_pool.submit(self.proc.communicate, data)
            result_val = eval(result[0].strip())
            print(result_val)
            if result_val<1:
                self.write("HAM")
            else:
                self.write("SPAM")

            self.finish()
        except Exception:
            print(str(Exception))
            print("-----------finish----------------")
            self.write("ERROR")
            self.finish()


        ################file version###################

        #fileinfo = self.request.files['file'][0]
        #print("fileinfo is", fileinfo)
        #fname = fileinfo['filename']
        #extn = os.path.splitext(fname)[1]
        #print(fname)
        #cname = str(uuid.uuid4()) + extn
        #fh = open(__UPLOADS__ + cname, 'w')
        #fh.write(fileinfo['body'])
        #self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)
        #self.write("rock the party, yo!")


######################THIS IS THE blocking version for testing purposes################
class SlowHandler(tornado.web.RequestHandler):
    def prepare(self):
        #setup command
        command = "spamc -c"
        args = shlex.split(command)

        #send command and get result
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def slow_method(self, data):
        arr = []
        for i in range(1,100):
            arr[0] = len(str(requests.get("http://www.google.co.uk")))

    def post(self):

        #############POST data ##########################
        try:
            #get data
            data = self.request.body

            result = self.proc.communicate(data)
            #result=self.slow_method(data)

            result_val = eval(result[0].strip())
            print(result_val)
            if result_val<1:
                self.write("HAM")
            else:
                self.write("SPAM")
        except Exception:
            print(Exception)
            self.write("ERROR")





application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/slow", SlowHandler),

], debug=True)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
