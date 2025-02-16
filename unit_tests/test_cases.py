import unittest
import pdb
import sys
import psychoacoustics.case
import psychoacoustics.failure
from psychoacoustics.pyversion import unbound_method
from psychoacoustics.config import Config
from mock import ResultProxyFactory, ResultProxy

class TestNoseCases(unittest.TestCase):

    def test_function_test_case(self):
        res = unittest.TestResult()
        
        a = []
        def func(a=a):
            a.append(1)

        case = psychoacoustics.case.FunctionTestCase(func)
        case(res)
        assert a[0] == 1

    def test_method_test_case(self):
        res = unittest.TestResult()

        a = []
        class TestClass(object):
            def test_func(self, a=a):
                a.append(1)

        case = psychoacoustics.case.MethodTestCase(unbound_method(TestClass,
                                                       TestClass.test_func))
        case(res)
        assert a[0] == 1

    def test_method_test_case_with_metaclass(self):
        res = unittest.TestResult()
        
        class TestType(type):
            def __new__(cls, name, bases, dct):
                return type.__new__(cls, name, bases, dct)
        a = []
        class TestClass(object):
            __metaclass__ = TestType
            def test_func(self, a=a):
                a.append(1)

        case = psychoacoustics.case.MethodTestCase(unbound_method(TestClass,
                                                       TestClass.test_func))
        case(res)
        assert a[0] == 1

    def test_method_test_case_fixtures(self):        
        res = unittest.TestResult()
        called = []
        class TestClass(object):
            def setup(self):
                called.append('setup')
            def teardown(self):
                called.append('teardown')
            def test_func(self):
                called.append('test')

        case = psychoacoustics.case.MethodTestCase(unbound_method(TestClass,
                                                       TestClass.test_func))
        case(res)
        self.assertEqual(called, ['setup', 'test', 'teardown'])

        class TestClassFailingSetup(TestClass):
            def setup(self):
                called.append('setup')
                raise Exception("failed")
        called[:] = []
        case = psychoacoustics.case.MethodTestCase(unbound_method(TestClassFailingSetup,
                                            TestClassFailingSetup.test_func))
        case(res)
        self.assertEqual(called, ['setup'])        

        class TestClassFailingTest(TestClass):
            def test_func(self):
                called.append('test')
                raise Exception("failed")
            
        called[:] = []
        case = psychoacoustics.case.MethodTestCase(unbound_method(TestClassFailingTest,
                                            TestClassFailingTest.test_func))
        case(res)
        self.assertEqual(called, ['setup', 'test', 'teardown'])     
        
    def test_function_test_case_fixtures(self):
        from psychoacoustics.tools import with_setup
        res = unittest.TestResult()

        called = {}

        def st():
            called['st'] = True
        def td():
            called['td'] = True

        def func_exc():
            called['func'] = True
            raise TypeError("An exception")

        func_exc = with_setup(st, td)(func_exc)
        case = psychoacoustics.case.FunctionTestCase(func_exc)
        case(res)
        assert 'st' in called
        assert 'func' in called
        assert 'td' in called

    def test_failure_case(self):
        res = unittest.TestResult()
        f = psychoacoustics.failure.Failure(ValueError, "No such test spam")
        f(res)
        assert res.errors

    def test_FunctionTestCase_repr_is_consistent_with_mutable_args(self):
        class Foo(object):
            def __init__(self):
                self.bar = 'unmodified'
            def __repr__(self):
                return "Foo(%s)" % self.bar

        def test_foo(foo):
            pass

        foo = Foo()
        case = psychoacoustics.case.FunctionTestCase(test_foo, arg=(foo,))
        case_repr_before = case.__repr__()
        foo.bar = "snafu'd!"
        case_repr_after = case.__repr__()
        assert case_repr_before == case_repr_after, (
            "Modifying a mutable object arg during test case changed the test "
            "case's __repr__")

    def test_MethodTestCase_repr_is_consistent_with_mutable_args(self):
        class Foo(object):
            def __init__(self):
                self.bar = 'unmodified'
            def __repr__(self):
                return "Foo(%s)" % self.bar

        class FooTester(object):
            def test_foo(self, foo):
                pass

        foo = Foo()
        case = psychoacoustics.case.FunctionTestCase(
            unbound_method(FooTester, FooTester.test_foo), arg=(foo,))
        case_repr_before = case.__repr__()
        foo.bar = "snafu'd!"
        case_repr_after = case.__repr__()
        assert case_repr_before == case_repr_after, (
            "Modifying a mutable object arg during test case changed the test "
            "case's __repr__")


class TestNoseTestWrapper(unittest.TestCase):
    def test_case_fixtures_called(self):
        """Instance fixtures are properly called for wrapped tests"""
        res = unittest.TestResult()
        called = []
                        
        class TC(unittest.TestCase):
            def setUp(self):
                print "TC setUp %s" % self
                called.append('setUp')
            def runTest(self):
                print "TC runTest %s" % self
                called.append('runTest')
            def tearDown(self):
                print "TC tearDown %s" % self
                called.append('tearDown')

        case = psychoacoustics.case.Test(TC())
        case(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        self.assertEqual(called, ['setUp', 'runTest', 'tearDown'])

    def test_result_proxy_used(self):
        """A result proxy is used to wrap the result for all tests"""
        class TC(unittest.TestCase):
            def runTest(self):
                raise Exception("error")
            
        ResultProxy.called[:] = []
        res = unittest.TestResult()
        config = Config()
        case = psychoacoustics.case.Test(TC(), config=config,
                              resultProxy=ResultProxyFactory())

        case(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures

        calls = [ c[0] for c in ResultProxy.called ]
        self.assertEqual(calls, ['beforeTest', 'startTest', 'addError',
                                 'stopTest', 'afterTest'])

    def test_address(self):
        from psychoacoustics.util import absfile, src
        class TC(unittest.TestCase):
            def runTest(self):
                raise Exception("error")

        def dummy(i):
            pass

        def test():
            pass

        class Test:
            def test(self):
                pass

            def test_gen(self):
                def tryit(i):
                    pass
                for i in range (0, 2):
                    yield tryit, i

            def try_something(self, a, b):
                pass

        fl = src(absfile(__file__))
        case = psychoacoustics.case.Test(TC())
        self.assertEqual(case.address(), (fl, __name__, 'TC.runTest'))

        case = psychoacoustics.case.Test(psychoacoustics.case.FunctionTestCase(test))
        self.assertEqual(case.address(), (fl, __name__, 'test'))

        case = psychoacoustics.case.Test(psychoacoustics.case.FunctionTestCase(
            dummy, arg=(1,), descriptor=test))
        self.assertEqual(case.address(), (fl, __name__, 'test'))

        case = psychoacoustics.case.Test(psychoacoustics.case.MethodTestCase(
                                  unbound_method(Test, Test.test)))
        self.assertEqual(case.address(), (fl, __name__, 'Test.test'))

        case = psychoacoustics.case.Test(
            psychoacoustics.case.MethodTestCase(unbound_method(Test, Test.try_something),
                                     arg=(1,2,),
                                     descriptor=unbound_method(Test,
                                                               Test.test_gen)))
        self.assertEqual(case.address(),
                         (fl, __name__, 'Test.test_gen'))

        case = psychoacoustics.case.Test(
            psychoacoustics.case.MethodTestCase(unbound_method(Test, Test.test_gen),
                                     test=dummy, arg=(1,)))
        self.assertEqual(case.address(),
                         (fl, __name__, 'Test.test_gen'))

    def test_context(self):
        class TC(unittest.TestCase):
            def runTest(self):
                pass
        def test():
            pass

        class Test:
            def test(self):
                pass

        case = psychoacoustics.case.Test(TC())
        self.assertEqual(case.context, TC)

        case = psychoacoustics.case.Test(psychoacoustics.case.FunctionTestCase(test))
        self.assertEqual(case.context, sys.modules[__name__])

        case = psychoacoustics.case.Test(psychoacoustics.case.MethodTestCase(unbound_method(Test,
                                                           Test.test)))
        self.assertEqual(case.context, Test)

    def test_short_description(self):
        class TC(unittest.TestCase):
            def test_a(self):
                """
                This is the description
                """
                pass

            def test_b(self):
                """This is the description
                """
                pass

            def test_c(self):
                pass

        case_a = psychoacoustics.case.Test(TC('test_a'))
        case_b = psychoacoustics.case.Test(TC('test_b'))
        case_c = psychoacoustics.case.Test(TC('test_c'))

        assert case_a.shortDescription().endswith("This is the description")
        assert case_b.shortDescription().endswith("This is the description")
        assert case_c.shortDescription() in (None, # pre 2.7
                                             'test_c (test_cases.TC)') # 2.7

    def test_unrepresentable_shortDescription(self):
        class TC(unittest.TestCase):
            def __str__(self):
                # see issue 422
                raise ValueError('simulate some mistake in this code')
            def runTest(self):
                pass

        case = psychoacoustics.case.Test(TC())
        self.assertEqual(case.shortDescription(), None)

if __name__ == '__main__':
    unittest.main()
