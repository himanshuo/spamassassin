from __future__ import print_function

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
from tornado.process import *

from tornado.gen import Task, Return, coroutine
import tornado.process
from tornado.ioloop import IOLoop
import subprocess
import time
import tornado.web
from pprint import pprint
thread_pool = ThreadPoolExecutor(4)
class GenAsyncHandler(tornado.web.RequestHandler):
    #THIS MIGHT BE NOT PARALLEL. 2ish reasons:
        # prepare is something that is run at start of server. NOT LIKELY A PROBLEM, BUT WHO KNOWS?
        # ACTUAL POTENTIAL PROBLEM: the stdin takes in a PIPE instead of a stream.

    # def prepare(self):
    #     #setup command
    #     command = "spamc -c"
    #     self.args = shlex.split(command)
    #     #self.STREAM = tornado.process.Subprocess.STREAM




    @coroutine
    def call_spamassassin(self, cmd='wc', stdin_data="123"):
        """
        Wrapper around subprocess call using Tornado's Subprocess class.
        """

        STREAM = tornado.process.Subprocess.STREAM


        args = shlex.split(cmd)
        proc = tornado.process.Subprocess(
            args, stdin=STREAM, stdout=STREAM, stderr=STREAM
        )


        pprint(proc.stdin)

        yield Task(proc.stdin.write, str.encode(stdin_data))

        print(1)
        proc.stdin.close()

        result, error = yield [
            Task(proc.stdout.read_until_close),
            Task(proc.stderr.read_until_close)
        ]
        print(2)
        # self.write("inside call_spammassssin")
        return result, error


    @gen.coroutine
    def get(self):


        email = self.get_argument("email", None)
        if email:
            result, error = yield gen.Task(self.call_spamassassin,'spamc', email)
            str_result = bytes.decode(result)
            self.write(email+":"+str_result)
            self.finish()
        else:
            self.write("email does not exist\n")
            self.finish()

    # @gen.coroutine
    # def get(self):
    #
    #     #do_something_with_response(response)
    #     if self.get_argument("id", "id does not exists") == "1":
    #         #self.write("sleeping .... ")
    #         self.flush()
    #         data = self.get_argument('email','hello good sire, i am an advertisement. buy buy buyb buyb buy buyb buy ')
    #
    #         result, error = yield self.call_spamassassin(cmd='wc', stdin_data='123')
    #         print('stdin async: ', result)
    #
    #         IOLoop.instance().stop()


            #send command and get result
            #proc = tornado.process.Subprocess(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            #result =proc.communicate(data)

            #self.proc = tornado.process.Subprocess(args)
            #pprint(self.proc.__dict__)

            #result = self.proc.proc.communicate(data)
            #print(2)
            #result = result[0].decode("utf-8").strip("\n")
            #result_val = eval(result)

            #if result_val<1:
            #    self.write("HAM")
            #else:
            #    self.write("SPAM")
            #self.finish()



    #working version of parallel example.
    # @gen.coroutine
    # def get(self):
    #     http_client = httpclient.AsyncHTTPClient()
    #     response = yield http_client.fetch("http://example.com")
    #     #do_something_with_response(response)
    #     if self.get_argument("id", "id does not exists") == "1":
    #         self.write("sleeping .... ")
    #         self.flush()
    #         # Do nothing for 5 sec
    #         yield gen.Task(IOLoop.instance().add_timeout, time.time() + 5)
    #         self.write("I'm awake!")
    #         self.finish()
    #     else:
    #         self.write(self.get_argument('id', "id does not exist")+" is the current id. NOT 1.\n")

application = tornado.web.Application([
    (r"/", GenAsyncHandler),


], debug=True, autoreload=True)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

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
"""
            # probably best to go through various ways of input in a method and use whichever one works.
            # data = self.get_body_arguments('email','')
            #print(data)
            #data = self.get_arguments('email','')
            #print(data)
"""
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
"""

# @coroutine
# def call_subprocess(cmd, stdin_data=None, stdin_async=False):
#     """
#     Wrapper around subprocess call using Tornado's Subprocess class.
#     """
#     stdin = STREAM if stdin_async else subprocess.PIPE
#
#     sub_process = tornado.process.Subprocess(
#         cmd, stdin=stdin, stdout=STREAM, stderr=STREAM
#     )
#
#     if stdin_data:
#         if stdin_async:
#             yield Task(sub_process.stdin.write, stdin_data)
#         else:
#             sub_process.stdin.write(stdin_data)
#
#     if stdin_async or stdin_data:
#         sub_process.stdin.close()
#
#     result, error = yield [
#         Task(sub_process.stdout.read_until_close),
#         Task(sub_process.stderr.read_until_close)
#     ]
#
#     raise Return((result, error))