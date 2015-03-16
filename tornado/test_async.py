from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
from tornado.ioloop import IOLoop
import subprocess
import time
import tornado.ioloop
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio


STREAM = tornado.process.Subprocess.STREAM


@coroutine
def call_subprocess(cmd, stdin_data=None):
    """
    Wrapper around subprocess call using Tornado's Subprocess class.
    """


    sub_process = tornado.process.Subprocess(
        cmd, stdin=STREAM, stdout=STREAM, stderr=STREAM
    )

    if stdin_data:
        yield Task(sub_process.stdin.write, stdin_data)


    if stdin_data:
        sub_process.stdin.close()

    result, error = yield [
        Task(sub_process.stdout.read_until_close),
        Task(sub_process.stderr.read_until_close)
    ]

    return (result, error)



@coroutine
def get_result():
    print("arg2 internal called")
    result, err = yield Task(call_subprocess, 'wc','123')
    print("arg2 internal done")
    #s.write("arg2 called"+str(a))
    return result
    #result = yield gen.Task(pool.apply_async, func, args, kwargs)


def print_stuff(future_result):
    print("printing stuff")

    a = yield future_result

    print(a)


class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):


        #result = call_subprocess('wc', stdin_data="123")
        #self.write('stdin sync: '+str(result))

        #self.write()

        if(self.get_argument("id") == "1"):
            print("arg1 occured")
            self.write("arg 1 occured")
        else:

            pass
            a = yield Task(get_result)

            # IOLoop.instance().add_future(a,print_stuff )




application = tornado.web.Application( [
    (r"/", MainHandler),
])



if __name__ == "__main__":
    # application.listen(8000)
    #
    # tornado.ioloop.IOLoop.instance().start()



    application.listen(8000)
    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.add_callback(get_result)
    io_loop.start()

    # IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
    # IOLoop.run_until_complete(get_result())
    # IOLoop.instance().start()
    # AsyncIOMainLoop().install()

