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
import json
import datetime

class GenAsyncHandler(tornado.web.RequestHandler):
    #THIS MIGHT BE NOT PARALLEL. 2ish reasons:
        # prepare is something that is run at start of server. NOT LIKELY A PROBLEM, BUT WHO KNOWS?
        # ACTUAL POTENTIAL PROBLEM: the stdin takes in a PIPE instead of a stream.

    def prepare(self):
        #setup command
        command = "spamc"
        args = shlex.split(command)
        STREAM = tornado.process.Subprocess.STREAM
        self.proc = tornado.process.Subprocess(
            args, stdin=STREAM, stdout=STREAM, stderr=STREAM
        )

        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }

    def _get_predefined_headers(self):
        out = ""
        for k,v in self.PREDEFINED_HEADERS.items():
            out+=self._format_header_val(k, v)
        return out

    def _url_params_to_text(self, data):
        out=""
        #i think it might be okay to have these url params as extra headers.
        dont_include = ['message', 'email']
        for k,v in data.items():
            if k not in dont_include:
                out+=self._format_header_val(k, v)
        return out



    # def _add_recieved_header(self,data):
    #     """
    # Received: from iron3.mail.virginia.edu (iron3.mail.Virginia.EDU. [128.143.2.240])
    #     by mx.google.com with ESMTP id c7si2000643qaj.77.2015.01.15.06.13.23
    #     for <ho2es@goog.email.virginia.edu>;
    #     Thu, 15 Jan 2015 06:13:23 -0800 (PST)
    #
    # """
    #     received = "Received: "
    #     if data.get('email'):
    #         received += "by " data.get('email')
    #         if data.get('')

    def _format_header_val(self,key, value ):
        return str(key)+": "+str(value)+"\n"

    def _get_custom_headers(self, data):
        #not predefined, but we really want it.
            #Received; by ip_address OR name \n date(Thu, 15 Jan 2015 06:13:23 -0800 (PST) )
            #Date same as data in the recieved.
            #X-Sender-IP
            #Subject: name_of_project

        #RULES THAT BREAK WITHOUT HEADERS:
        """
        -0.0 NO_RELAYS              Informational: message was not relayed via SMTP                           score 0
         1.2 MISSING_HEADERS        Missing To: header                                                        score 0
         1.4 MISSING_DATE           Missing Date: header                                                      score 0
        -0.0 NO_RECEIVED            Informational: message has no Received headers                            score 0
         0.1 MISSING_MID            Missing Message-Id: header                                                time+
         1.8 MISSING_SUBJECT        Missing Subject: header                                                   project
         1.0 MISSING_FROM           Missing From: header
         0.0 NO_HEADERS_MESSAGE     Message appears to be missing most RFC-822 headers



        author: commenter name
                email: commenter email
                subject: project on which person is
                ip: ip address of author.
                Content-Type: text/plain
        """
        header=""
        header+=self._get_predefined_headers()
        header+=self._url_params_to_text(data)
        if data.get('email'):
            header+= self._format_header_val("Email",data.get('email'))
        if data.get('project_name'):
            header+=self._format_header_val("Subject",data.get('project_name'))
        if data.get('contributors'):
            header+=self._format_header_val("From", data.get('contributors'))


        #header+=self._add_recieved_header()

        return header

    @coroutine
    def call_spamassassin(self, data):
        """
        Wrapper around subprocess call using Tornado's Subprocess class.
        """

        #add headers to stdin_data
        #bytes to string. then add header strings then \n then reconvert to bytes
        #message = str.decode(stdin_data,'utf-8')

        message_with_header = self._get_custom_headers(data) +"\n" + data['message']

        stdin_data = str.encode(message_with_header)

        yield Task(self.proc.stdin.write, stdin_data)


        self.proc.stdin.close()

        result, error = yield [
            Task(self.proc.stdout.read_until_close),
            Task(self.proc.stderr.read_until_close)
        ]

        # self.write("inside call_spammassssin")

        return result, error


    def _handle_result(self, res):
        str_result = bytes.decode(res)
        print(str_result)
        result_val = eval(str_result.strip())

        if result_val<1:
            return "HAM"
        else:
            return "SPAM"

    @gen.coroutine
    def post(self):



        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        if 'message' in data:

            #this is just for testing purposes. delete once done testing.
            # if email_bytes.decode('utf-8') == "data=1":
            #     #print("long called")
            #     f=open('too_long.txt')
            #     result, error = yield gen.Task(self.call_spamassassin,str.encode(f.read()))
            # else:
            #     result, error = yield gen.Task(self.call_spamassassin,email_bytes)
            # print(result)

            result,error = yield gen.Task(self.call_spamassassin,data )
            self.write(self._handle_result(result))
            self.finish()
        else:
            self.write("No Message Given\n")
            self.finish()








application = tornado.web.Application([
    (r"/", GenAsyncHandler)
], debug=True, autoreload=True)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
