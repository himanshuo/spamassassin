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

        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }


    def _get_proc(self, full_report):

        STREAM = tornado.process.Subprocess.STREAM

        cur_proc = None
        if full_report:
            #full report version
            cur_proc = tornado.process.Subprocess(
                shlex.split("spamc"), stdin=STREAM, stdout=STREAM, stderr=STREAM
            )
        else:
            #normal version
            command = "spamc -c"
            args = shlex.split(command)
            cur_proc = tornado.process.Subprocess(
                args, stdin=STREAM, stdout=STREAM, stderr=STREAM
            )

        return cur_proc









    def _format_header_val(self,key, value ):
        try:
            key = str(key).capitalize()
            if isinstance(value, (list, tuple)):
                out = key+": "
                for v in value:
                    out+= str(v) + ", "
                out = str[0:-2] + "\n"
                return out
            else:
                return key+": "+str(value)+"\n"
        except:
            print(key,"::::::::::::::::::::", value)
            return ""



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
        cur_proc = self._get_proc(full_report)


        yield Task(cur_proc.stdin.write, stdin_data)


        cur_proc.stdin.close()


        result, error = yield [
            Task(cur_proc.stdout.read_until_close),
            Task(cur_proc.stderr.read_until_close)
        ]

        cur_proc.stdout.close()
        cur_proc.stderr.close()



        return result, error


    def _handle_result(self, res):
        str_result = bytes.decode(res)

        result_val = eval(str_result.strip())

        if result_val<1:
            return "HAM"
        else:
            return "SPAM"


    def _file_to_data(self, file_contents):

        data = {}
        lineno = 0

        lines = file_contents.splitlines()

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

    @gen.coroutine
    def post(self):
        try:



            data = None

            if self.get_argument('is_file', False):
                file_contents = self.request.files['file'][0]['body']
                file_contents = file_contents.decode('utf-8','ignore')

                data= self._file_to_data(file_contents)


            else:
                data = json.loads(self.request.body.decode('utf-8', 'ignore'))



            if 'message' in data or self.get_argument('is_file',False):

                if self.get_argument('full_report',False):
                    result,error = yield gen.Task(self.call_spamassassin,data,full_report=True )
                    self.write(result)
                else:
                    result,error = yield gen.Task(self.call_spamassassin,data,full_report=False )
                    self.write(self._handle_result(result))


                self.finish()
            else:
                self.write("No Message Given\n")
                self.finish()
        except:
            self.set_status(400)
            self.finish("Malformed Request")



class TeacherHandler(MainHandler):

    def prepare(self):
        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }

    #todo: see if you can optimize (and not have security issue) by having 2 global proc objects.
    def _get_proc(self, is_spam):

        STREAM = tornado.process.Subprocess.STREAM
        command = "sudo ./call_sa-learn.sh"
        if is_spam:
            command+=" --spam"
        else:
            command+=" --ham"

        args = shlex.split(command)
        proc = tornado.process.Subprocess(
            args, stdin=STREAM, stdout=STREAM, stderr=STREAM
        )
        return proc


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

        cur_proc = self._get_proc(data.pop('is_spam'))



        message_with_header = self._get_custom_headers(data) +"\n" + str(data.get('message',""))

        stdin_data = str.encode(message_with_header)

        yield Task(cur_proc.stdin.write, stdin_data)


        cur_proc.stdin.close()

        result, error = yield [
            Task(cur_proc.stdout.read_until_close),
            Task(cur_proc.stderr.read_until_close)
        ]

        cur_proc.stdout.close()
        cur_proc.stderr.close()


        return result, error


    @gen.coroutine
    def post(self):

        data = json.loads(self.request.body.decode('utf-8'))

        if 'message' in data:
            result,error = yield gen.Task(self.teach_spamassassin,data )


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
