import os

from tempfile import mktemp
from time import sleep

if 'PSY_ECHOS_TICKS_MP_LOG' not in os.environ:
    raise Exception('Environment variable PSY_ECHOS_TICKS_MP_LOG is not set')

logfile = os.environ['PSY_ECHOS_TICKS_MP_LOG']
killfile = os.environ['PSY_ECHOS_TICKS_MP_KILL']

def log(w):
    f = open(logfile, 'a')
    f.write(w+"\n")
    f.close()

def touch_killfile():
    f = open(killfile,'wb')
    f.close()

#make sure all tests in this file are dispatched to the same subprocess
def setup():
    log('setup')

def test_timeout():
    log('test_timeout')
    touch_killfile()
    sleep(2)
    log('test_timeout_finished')

# check timeout will not prevent remaining tests dispatched to the same subprocess to continue to run
def test_pass():
    log('test_pass')

def teardown():
    log('teardown')
