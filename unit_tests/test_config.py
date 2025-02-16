import re
import os
import tempfile
import unittest
import warnings
import pickle
import sys

import psychoacoustics.config
from psychoacoustics.plugins.manager import DefaultPluginManager
from psychoacoustics.plugins.skip import SkipTest
from psychoacoustics.plugins.prof import Profile


class TestNoseConfig(unittest.TestCase):

    def test_defaults(self):
        c = psychoacoustics.config.Config()
        assert c.addPaths == True
        # FIXME etc

    def test_reset(self):
        c = psychoacoustics.config.Config()
        c.include = 'include'
        assert c.include == 'include'
        c.reset()
        assert c.include is None

    def test_update(self):
        c = psychoacoustics.config.Config()
        c.update({'exclude':'x'})
        assert c.exclude == 'x'

    def test_ignore_files_default(self):
        """
        The default configuration should have several ignore file settings.
        """
        c = psychoacoustics.config.Config()
        c.configure(['program'])
        self.assertEqual(len(c.ignoreFiles), 3)
    
    def test_ignore_files_single(self):
        """A single ignore-files flag should override the default settings.""" 
        c = psychoacoustics.config.Config()
        c.configure(['program', '--ignore-files=a'])
        self.assertEqual(len(c.ignoreFiles), 1)
        aMatcher = c.ignoreFiles[0]
        assert aMatcher.match('a')
        assert not aMatcher.match('b')
    
    def test_ignore_files_multiple(self):
        """
        Multiple ignore-files flags should be appended together, overriding
        the default settings.
        """
        c = psychoacoustics.config.Config()
        c.configure(['program', '--ignore-files=a', '-Ib'])
        self.assertEqual(len(c.ignoreFiles), 2)
        aMatcher, bMatcher = c.ignoreFiles
        assert aMatcher.match('a')
        assert not aMatcher.match('b')
        assert bMatcher.match('b')
        assert not bMatcher.match('a')
    
    def test_multiple_include(self):
        c = psychoacoustics.config.Config()
        c.configure(['program', '--include=a', '--include=b'])
        self.assertEqual(len(c.include), 2)
        a, b = c.include
        assert a.match('a')
        assert not a.match('b')
        assert b.match('b')
        assert not b.match('a')

    def test_single_include(self):
        c = psychoacoustics.config.Config()
        c.configure(['program', '--include=b'])
        self.assertEqual(len(c.include), 1)
        b = c.include[0]
        assert b.match('b')
        assert not b.match('a')

    def test_plugins(self):
        c = psychoacoustics.config.Config()
        assert c.plugins
        c.plugins.begin()

    def test_testnames(self):
        c = psychoacoustics.config.Config()
        c.configure(['program', 'foo', 'bar', 'baz.buz.biz'])
        self.assertEqual(c.testNames, ['foo', 'bar', 'baz.buz.biz'])

        c = psychoacoustics.config.Config(testNames=['foo'])
        c.configure([])
        self.assertEqual(c.testNames, ['foo'])

    def test_where(self):
        # we don't need to see our own warnings
        warnings.filterwarnings(action='ignore',
                                category=DeprecationWarning,
                                module='psychoacoustics.config')

        here = os.path.dirname(__file__)
        support = os.path.join(here, 'support')
        foo = os.path.abspath(os.path.join(support, 'foo'))
        c = psychoacoustics.config.Config()
        c.configure(['program', '-w', foo, '-w', 'bar'])
        self.assertEqual(c.workingDir, foo)
        self.assertEqual(c.testNames, ['bar'])

    def test_progname_looks_like_option(self):
        # issue #184
        c = psychoacoustics.config.Config()
        # the -v here is the program name, not an option
        # this matters eg. with python -c "import psychoacoustics; psychoacoustics.main()"
        c.configure(['-v', 'mytests'])
        self.assertEqual(c.verbosity, 1)

    def test_pickle_empty(self):
        c = psychoacoustics.config.Config()
        cp = pickle.dumps(c)
        cc = pickle.loads(cp)

    def test_pickle_configured(self):
        if 'java' in sys.version.lower():
            raise SkipTest("jython has no profiler plugin")
        c = psychoacoustics.config.Config(plugins=DefaultPluginManager())
        config_args = ['--with-doctest', '--with-coverage', 
                     '--with-id', '--attr=A', '--collect', '--all',
                     '--with-isolation', '-d', '--with-xunit', '--processes=2',
                     '--pdb']
        if Profile.available():
            config_args.append('--with-profile')
        c.configure(config_args)
        cp = pickle.dumps(c)
        cc = pickle.loads(cp)
        assert cc.plugins._plugins


if __name__ == '__main__':
    unittest.main()
