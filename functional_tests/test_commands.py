import os
import sys
import unittest
from psychoacoustics.plugins.skip import SkipTest
from psychoacoustics import commands
from StringIO import StringIO

support = os.path.join(
    os.path.dirname(__file__), 'support', 'issue191')


class TestCommands(unittest.TestCase):
    def setUp(self):
        try:
            import setuptools
        except ImportError:
            raise SkipTest("setuptools not available")
        self.dir = os.getcwd()
        self.stderr = sys.stderr
        os.chdir(support)

    def tearDown(self):
        os.chdir(self.dir)
        sys.stderr = self.stderr
    
    def test_setup_psytests_command_works(self):
        from setuptools.dist import Distribution
        buf = StringIO()
        sys.stderr = buf
        cmd = commands.psytests(
            Distribution(attrs={'script_name': 'setup.py',
                                'package_dir': {'issue191': support}}))
        cmd.finalize_options()
        ## FIXME why doesn't Config see the chdir above?
        print cmd._psytests__config.workingDir
        cmd._psytests__config.workingDir = support
        cmd._psytests__config.stream = buf
        try:
            cmd.run()
        except SystemExit, e:
            self.assertFalse(e.args[0], buf.getvalue())
        else:
            self.fail("cmd.run() did not exit")


if __name__ == '__main__':
    unittest.main()
