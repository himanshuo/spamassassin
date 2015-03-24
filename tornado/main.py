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

class MainHandler(tornado.web.RequestHandler):
    #THIS MIGHT BE NOT PARALLEL. 2ish reasons:
        # prepare is something that is run at start of server. NOT LIKELY A PROBLEM, BUT WHO KNOWS?
        # ACTUAL POTENTIAL PROBLEM: the stdin takes in a PIPE instead of a stream.

    def prepare(self):
        #setup command


        command = "spamc -c"
        args = shlex.split(command)


        self.STREAM = tornado.process.Subprocess.STREAM

        self.proc = tornado.process.Subprocess(
            args, stdin=self.STREAM, stdout=self.STREAM, stderr=self.STREAM
        )

        self.full_report_proc = tornado.process.Subprocess(
            shlex.split("spamc"), stdin=self.STREAM, stdout=self.STREAM, stderr=self.STREAM
        )

        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }






    def _format_header_val(self,key, value ):
        key = str(key).capitalize()
        if isinstance(value, (list, tuple)):
            out = key+": "
            for v in value:
                out+= str(v) + ", "
            out = str[0:-2] + "\n"
            return out
        else:
            return key+": "+str(value)+"\n"



    def _get_predefined_headers(self):
        out = ""
        for k,v in self.PREDEFINED_HEADERS.items():
            out+=self._format_header_val(k, v)
        return out

    def _url_params_to_text(self, data):
        out=""
        #i think it might be okay to have these url params as extra headers.
        dont_include = ['message']
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
            header+= self._format_header_val("From",data.get('email'))
        if data.get('project_name'):
            header+=self._format_header_val("Subject",data.get('project_name'))

        #header+=self._add_recieved_header()

        return header



    @coroutine
    def call_spamassassin(self, data, full_report=False):
        """
        Wrapper around subprocess call using Tornado's Subprocess class.
        """
        #add headers to stdin_data
        #bytes to string. then add header strings then \n then reconvert to bytes
        #message = str.decode(stdin_data,'utf-8')
        message_with_header = self._get_custom_headers(data) +"\n" + data['message']
        stdin_data = str.encode(message_with_header)
        cur_proc = self.proc
        if full_report:
            cur_proc = self.full_report_proc

        yield Task(cur_proc.stdin.write, stdin_data)


        cur_proc.stdin.close()

        result, error = yield [
            Task(cur_proc.stdout.read_until_close),
            Task(cur_proc.stderr.read_until_close)
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

            if 'full_report' in data and data.get('full_report'):
                result,error = yield gen.Task(self.call_spamassassin,data,full_report=True )
            else:
                result,error = yield gen.Task(self.call_spamassassin,data,full_report=False )

            self.write(self._handle_result(result))
            self.finish()
        else:
            self.write("No Message Given\n")
            self.finish()



class TeacherHandler(MainHandler):

    def prepare(self):



        command = "sa-learn"


        self.STREAM = tornado.process.Subprocess.STREAM
        self.teaching_spam_proc = tornado.process.Subprocess(
            shlex.split(command+" --spam"), stdin=self.STREAM, stdout=self.STREAM, stderr=self.STREAM
        )
        self.teaching_ham_proc = tornado.process.Subprocess(
            shlex.split(command+" --ham"), stdin=self.STREAM, stdout=self.STREAM, stderr=self.STREAM
        )

        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }


    @coroutine
    def teach_spamassassin(self, data):
        """
        NOTE: http://askubuntu.com/questions/159007/how-do-i-run-specific-sudo-commands-without-a-password
        sa-learn requires sudo. In this case, I just made it so that for this specific command (sa-learn)
        we do not need to use sudo. O
        Other way to handle this is to call sudo using process and then input a password. This is bad way.
        :param data:
        :return:
        """
        cur_proc = None
        if data.get('spam'):
            cur_proc = self.teaching_spam_proc
        else:
            cur_proc = self.teaching_ham_proc

        message_with_header = self._get_custom_headers(data) +"\n" + data['message']
        stdin_data = str.encode(message_with_header)

        yield Task(cur_proc.stdin.write, stdin_data)

        cur_proc.stdin.close()
        result, error = yield [
            Task(cur_proc.stdout.read_until_close),
            Task(cur_proc.stderr.read_until_close)
        ]

        return result, error


    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        if 'message' in data:
            result,error = yield gen.Task(self.teach_spamassassin,data )

            print("-----------------------------------")
            print(error)
            print("-----------------------------------")
            if not error:
                self.write("Learned")
                self.finish()
            else:
                self.set_status(400)
                self.finish("Malformed Request")
        else:
            self.write("No Message Given\n")
            self.finish()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/teach", TeacherHandler)
], debug=True, autoreload=True)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
