"""
Examples of test function/method attribute usage with patched psychoacoustics

Simple syntax (-a, --attr) examples:
  * psytests -a status=stable
    => only test cases with attribute "status" having value "stable"

  * psytests -a priority=2,status=stable
    => both attributes must match

  * psytests -a tags=http
    => attribute list "tags" must contain value "http" (see test_foobar()
       below for definition)

  * psytests -a slow
    => attribute "slow" must be defined and its value cannot equal to False
       (False, [], "", etc...)

  * psytests -a !slow
    => attribute "slow" must NOT be defined or its value must be equal to False

Eval expression syntax (-A, --eval-attr) examples:
  * psytests -A "not slow"
  * psytests -A "(priority > 5) and not slow"
  
This example and the accompanied patch is in public domain, free for any use.

email: mika.eloranta@gmail.com

"""

__author__ = 'Mika Eloranta'

def attr(**kwargs):
    """Add attributes to a test function/method/class"""
    def wrap(func):
        func.__dict__.update(kwargs)
        return func
    return wrap

# test function with single attribute
@attr(priority = 1)
def test_dummy():
    print "dummy"
    
# test function with multiple attributes
@attr(status = "stable",              # simple string attribute
      slow = True,                    # attributes can be of any type
                                      #   (e.g. bool)
      priority = 1,                   # ...or int
      tags = ["http", "pop", "imap"]) # will be run if any of the list items
                                      #   matches
def test_foobar():
    print "foobar"

# another way of adding attributes...
def test_fluffy():
    print "fluffy"
test_fluffy.status = "unstable"
test_fluffy.slow = True
test_fluffy.priority = 2

# works for class methods, too
class TestSomething:
    @attr(status = "stable", priority = 2)
    def test_xyz(self):
        print "xyz"

# class methods "inherit" attributes from the class but can override them
class TestOverride:
    value = "class"
    # run all methods with "psytests -a value"

    @attr(value = "method")
    def test_override(self):
        # run with "psytests -a value=method"
        print "override"
    
    def test_inherit(self):
        # run with "psytests -a value=class"
        print "inherit"
    
