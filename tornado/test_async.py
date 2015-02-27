from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
from tornado.ioloop import IOLoop
import subprocess
import time
import tornado.web
 
STREAM = tornado.process.Subprocess.STREAM
 
 
@coroutine
def call_subprocess(cmd, stdin_data=None, stdin_async=False):
    """
    Wrapper around subprocess call using Tornado's Subprocess class.
    """
    stdin = STREAM if stdin_async else subprocess.PIPE
 
    sub_process = tornado.process.Subprocess(
        cmd, stdin=stdin, stdout=STREAM, stderr=STREAM
    )
 
    if stdin_data:
        if stdin_async:
            yield Task(sub_process.stdin.write, stdin_data)
        else:
            sub_process.stdin.write(stdin_data)
 
    if stdin_async or stdin_data:
        sub_process.stdin.close()
 
    result, error = yield [
        Task(sub_process.stdout.read_until_close),
        Task(sub_process.stderr.read_until_close)
    ]
 
    raise Return((result, error))
 
 
def on_timeout():
    print("timeout")
    IOLoop.instance().stop()
 
 
@coroutine
class Main(tornado.web.RequestHandler):
    def get(self):
        seconds_to_wait = 10
        deadline = time.time() + seconds_to_wait

        # don't wait too long
        IOLoop.instance().add_timeout(deadline, on_timeout)


        # try to get output using asynchronous STREAM for stdin
        result, error = yield call_subprocess('wc', stdin_data="123", stdin_async=True)
        print('stdin async: ', result, error)


         # try to get output using synchronous PIPE for stdin
        #result, error = yield call_subprocess('spamc', stdin_data="123", stdin_async=True)
        #print('stdin sync: ', result, error)


        #IOLoop.instance().stop()

application = tornado.web.Application([
    (r"/", Main)
])

if __name__ == "__main__":
    application.listen(8000)
    ioloop = IOLoop.instance() 
    #ioloop.add_callback(Main.get())
    ioloop.start()