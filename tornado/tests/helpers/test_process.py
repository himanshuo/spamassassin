__author__ = 'himanshu'
import tornado.process
import shlex
import subprocess
from tornado.gen import Task, Return, coroutine

command = "spamc -c"
args = shlex.split(command)
STREAM = tornado.process.Subprocess.STREAM

proc = tornado.process.Subprocess(args, stdin=STREAM, stdout=STREAM)
def myinputfunc():
    yield Task(proc.stdin.write, "hi my name is himanshu")
def myoutputfunc():
    result, error = yield Task(proc.stdout.read_until_close)
    raise Return((result, error))

myinputfunc()
myoutputfunc()