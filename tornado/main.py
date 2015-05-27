from __future__ import print_function
import tornado.web
from tornado import gen
import shlex  # for calling spamc
from tornado.gen import Task, coroutine
import tornado.process
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.PREDEFINED_HEADERS = {
            'Content-Type': 'text/plain; charset=UTF-8',
            'MIME-Version': 1.0
        }

    def _get_proc(self, full_report):
        """Get process object based on type of process
        """
        STREAM = tornado.process.Subprocess.STREAM
        if full_report:
            # full report version
            cur_proc = tornado.process.Subprocess(
                shlex.split("spamc"),
                stdin=STREAM,
                stdout=STREAM,
                stderr=STREAM
            )
        else:
            # normal version
            command = "spamc -c"
            args = shlex.split(command)
            cur_proc = tornado.process.Subprocess(
                args, stdin=STREAM, stdout=STREAM, stderr=STREAM
            )
        return cur_proc

    def _format_header_val(self, key, value):
        """ format each header value
        """
        try:
            key = str(key).capitalize()
            if isinstance(value, (list, tuple)):
                out = key+": "
                if len(value) == 0:
                    return out
                for v in value:
                    out += str(v) + ", "
                out = str(out[0:-2]) + "\n"
                return out
            else:
                return key+": " + str(value) + "\n"
        except:
            return ""

    def _get_predefined_headers(self):
        out = ""
        for k, v in self.PREDEFINED_HEADERS.items():
            out += self._format_header_val(k, v)
        return out

    def _url_params_to_text(self, data):
        out = ""
        dont_include = ['message']
        for k, v in data.items():
            if k not in dont_include:
                out += self._format_header_val(k, v)
        return out

    def _get_custom_headers(self, data):
        """convert all key-value pairs attained from the data
         that are not 'message' into headers
        """
        header = ""
        header += self._get_predefined_headers()
        header += self._url_params_to_text(data)
        if data.get('email'):
            header += self._format_header_val("From", data.get('email'))
        if data.get('project_name'):
            header += self._format_header_val("Subject",
                                              data.get('project_name'))
        return header

    @coroutine
    def call_spamassassin(self, data, full_report=False):
        """
        Wrapper around subprocess call using Tornado's Subprocess class.
        """
        message_with_header = self._get_custom_headers(data) \
            + "\n" \
            + str(data['message'])
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
        """return HAM if spam_assassin determines message is ham. else SPAM
        """
        str_result = bytes.decode(res)

        result_val = eval(str_result.strip())

        if result_val < 1:
            return json.dumps({
                "decision": "HAM",
                "message": "The given message is HAM"

            })
        else:
            return json.dumps({
                "decision": "SPAM",
                "message": "The given message is SPAM"

            })

    def _file_to_data(self, file_contents):
        """Convert input data as a file into the data format
        usable for call_spamassassin
        """
        data = {}
        lineno = 0

        lines = file_contents.splitlines()

        for l in lines:
            lineno += 1
            if l == "\n" or l == "":
                break
            parts = l.split(":")
            if len(parts) > 1:
                key = parts[0].rstrip('\n')
                key = key.lower()
                value = parts[1].rstrip('\n')
                data[key] = value

        message = '\n'.join(lines[lineno:])
        message = message.rstrip('\n')
        data['message'] = message
        return data

    @gen.coroutine
    def post(self):
        try:
            data = None
            if self.get_argument('is_file', False):
                file_contents = self.request.files['file'][0]['body']
                file_contents = file_contents.decode('utf-8', 'ignore')

                data = self._file_to_data(file_contents)
            else:
                data = json.loads(self.request.body.decode('utf-8', 'ignore'))
            if 'message' in data or self.get_argument('is_file', False):
                if self.get_argument('full_report', False):
                    result, error = yield gen.Task(self.call_spamassassin,
                                                   data,
                                                   full_report=True)
                    self.write(result)
                else:
                    result, error = yield gen.Task(self.call_spamassassin,
                                                   data,
                                                   full_report=False)
                    self.set_header("Content-Type", "application/json")
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

    def _get_proc(self, is_spam):
        """ create and return process object based on whether input is spam or ham
        """

        STREAM = tornado.process.Subprocess.STREAM
        command = "sudo ./call_sa-learn.sh"
        if is_spam:
            command += " --spam"
        else:
            command += " --ham"

        args = shlex.split(command)
        proc = tornado.process.Subprocess(
            args, stdin=STREAM, stdout=STREAM, stderr=STREAM
        )
        return proc

    @coroutine
    def teach_spamassassin(self, data):
        """
        teach spam assassin whether current message is spam or not.

        NOTE:
        http://askubuntu.com/questions/159007/how-do-i-run-specific-sudo-commands-without-a-password
        sa-learn requires sudo. In this case, I just made it so that for this
        specific command (sa-learn) we do not need to use sudo.
        """
        cur_proc = self._get_proc(data.pop('is_spam'))
        message_with_header = self._get_custom_headers(data) \
            + "\n" + str(data.get('message', ""))
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
            result, error = yield gen.Task(self.teach_spamassassin, data)
            if not error:
                self.set_header("Content-Type", "application/json")
                self.write(
                    json.dumps({
                        "status": "Learned",
                        "message": "Spam Assassin trained using given message"
                    })
                )
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
