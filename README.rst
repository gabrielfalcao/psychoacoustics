Basic usage
***********

Use the psytests script (after installation by setuptools):

   psytests [options] [(optional) test files or directories]

In addition to passing command-line options, you may also put
configuration options in a .psychoacousticsrc or psychoacoustics.cfg file in your home
directory. These are standard .ini-style config files. Put your
psytests configuration in a [psytests] section, with the -- prefix
removed:

   [psytests]
   verbosity=3
   with-doctest=1

There is also possiblity to disable configuration files loading (might
be useful when runnig i.e. tox and you don't want your global psychoacoustics
config file to be used by tox). In order to ignore those configuration
files simply set an environment variable "PSY_ECHOS_TICKS_IGNORE_CONFIG_FILES".

There are several other ways to use the psychoacoustics test runner besides the
*psytests* script. You may use psychoacoustics in a test script:

   import psychoacoustics
   psychoacoustics.main()

If you don't want the test script to exit with 0 on success and 1 on
failure (like unittest.main), use psychoacoustics.run() instead:

   import psychoacoustics
   result = psychoacoustics.run()

*result* will be true if the test run succeeded, or false if any test
failed or raised an uncaught exception. Lastly, you can run psychoacoustics.core
directly, which will run psychoacoustics.main():

   python /path/to/psychoacoustics/core.py

Please see the usage message for the psytests script for information
about how to control which tests psychoacoustics runs, which plugins are loaded,
and the test output.


Extended usage
==============

psychoacoustics collects tests automatically from python source files,
directories and packages found in its working directory (which
defaults to the current working directory). Any python source file,
directory or package that matches the testMatch regular expression (by
default: *(?:\b|_)[Tt]est* will be collected as a test (or source for
collection of tests). In addition, all other packages found in the
working directory will be examined for python source files or
directories that match testMatch. Package discovery descends all the
way down the tree, so package.tests and package.sub.tests and
package.sub.sub2.tests will all be collected.

Within a test directory or package, any python source file matching
testMatch will be examined for test cases. Within a test module,
functions and classes whose names match testMatch and TestCase
subclasses with any name will be loaded and executed as tests. Tests
may use the assert keyword or raise AssertionErrors to indicate test
failure. TestCase subclasses may do the same or use the various
TestCase methods available.

**It is important to note that the default behavior of psychoacoustics is to not
include tests from files which are executable.**  To include tests
from such files, remove their executable bit or use the --exe flag
(see 'Options' section below).


Selecting Tests
---------------

To specify which tests to run, pass test names on the command line:

   psytests only_test_this.py

Test names specified may be file or module names, and may optionally
indicate the test case to run by separating the module or file name
from the test case name with a colon. Filenames may be relative or
absolute. Examples:

   psytests test.module
   psytests another.test:TestCase.test_method
   psytests a.test:TestCase
   psytests /path/to/test/file.py:test_function

You may also change the working directory where psychoacoustics looks for tests
by using the -w switch:

   psytests -w /path/to/tests

Note, however, that support for multiple -w arguments is now
deprecated and will be removed in a future release. As of psychoacoustics 0.10,
you can get the same behavior by specifying the target directories
*without* the -w switch:

   psytests /path/to/tests /another/path/to/tests

Further customization of test selection and loading is possible
through the use of plugins.

Test result output is identical to that of unittest, except for the
additional features (error classes, and plugin-supplied features such
as output capture and assert introspection) detailed in the options
below.


Configuration
-------------

In addition to passing command-line options, you may also put
configuration options in your project's *setup.cfg* file, or a .psychoacousticsrc
or psychoacoustics.cfg file in your home directory. In any of these standard ini-
style config files, you put your psytests configuration in a
"[psytests]" section. Options are the same as on the command line,
with the -- prefix removed. For options that are simple switches, you
must supply a value:

   [psytests]
   verbosity=3
   with-doctest=1

All configuration files that are found will be loaded and their
options combined. You can override the standard config file loading
with the "-c" option.


Using Plugins
-------------

There are numerous psychoacoustics plugins available via easy_install and
elsewhere. To use a plugin, just install it. The plugin will add
command line options to psytests. To verify that the plugin is
installed, run:

   psytests --plugins

You can add -v or -vv to that command to show more information about
each plugin.

If you are running psychoacoustics.main() or psychoacoustics.run() from a script, you can
specify a list of plugins to use by passing a list of plugins with the
plugins keyword argument.


0.9 plugins
-----------

psychoacoustics 1.0 can use SOME plugins that were written for psychoacoustics 0.9. The
default plugin manager inserts a compatibility wrapper around 0.9
plugins that adapts the changed plugin api calls. However, plugins
that access psychoacoustics internals are likely to fail, especially if they
attempt to access test case or test suite classes. For example,
plugins that try to determine if a test passed to startTest is an
individual test or a suite will fail, partly because suites are no
longer passed to startTest and partly because it's likely that the
plugin is trying to find out if the test is an instance of a class
that no longer exists.


0.10 and 0.11 plugins
---------------------

All plugins written for psychoacoustics 0.10 and 0.11 should work with psychoacoustics 1.0.


Options
-------

-V, --version

   Output psychoacoustics version and exit

-p, --plugins

   Output list of available plugins and exit. Combine with higher
   verbosity for greater detail

-v=DEFAULT, --verpsychoacoustics=DEFAULT

   Be more verpsychoacoustics. [PSY_ECHOS_TICKS_VERPSY_ECHOS_TICKS]

--verbosity=VERBOSITY

   Set verbosity; --verbosity=2 is the same as -v

-q=DEFAULT, --quiet=DEFAULT

   Be less verpsychoacoustics

-c=FILES, --config=FILES

   Load configuration from config file(s). May be specified multiple
   times; in that case, all config files will be loaded and combined

-w=WHERE, --where=WHERE

   Look for tests in this directory. May be specified multiple times.
   The first directory passed will be used as the working directory,
   in place of the current working directory, which is the default.
   Others will be added to the list of tests to execute. [PSY_ECHOS_TICKS_WHERE]

--py3where=PY3WHERE

   Look for tests in this directory under Python 3.x. Functions the
   same as 'where', but only applies if running under Python 3.x or
   above.  Note that, if present under 3.x, this option completely
   replaces any directories specified with 'where', so the 'where'
   option becomes ineffective. [PSY_ECHOS_TICKS_PY3WHERE]

-m=REGEX, --match=REGEX, --testmatch=REGEX

   Files, directories, function names, and class names that match this
   regular expression are considered tests.  Default: (?:\b|_)[Tt]est
   [PSY_ECHOS_TICKS_TESTMATCH]

--tests=NAMES

   Run these tests (comma-separated list). This argument is useful
   mainly from configuration files; on the command line, just pass the
   tests to run as additional arguments with no switch.

-l=DEFAULT, --debug=DEFAULT

   Activate debug logging for one or more systems. Available debug
   loggers: psychoacoustics, psychoacoustics.importer, psychoacoustics.inspector, psychoacoustics.plugins,
   psychoacoustics.result and psychoacoustics.selector. Separate multiple names with a
   comma.

--debug-log=FILE

   Log debug messages to this file (default: sys.stderr)

--logging-config=FILE, --log-config=FILE

   Load logging config from this file -- bypasses all other logging
   config settings.

-I=REGEX, --ignore-files=REGEX

   Completely ignore any file that matches this regular expression.
   Takes precedence over any other settings or plugins. Specifying
   this option will replace the default setting. Specify this option
   multiple times to add more regular expressions [PSY_ECHOS_TICKS_IGNORE_FILES]

-e=REGEX, --exclude=REGEX

   Don't run tests that match regular expression [PSY_ECHOS_TICKS_EXCLUDE]

-i=REGEX, --include=REGEX

   This regular expression will be applied to files, directories,
   function names, and class names for a chance to include additional
   tests that do not match TESTMATCH.  Specify this option multiple
   times to add more regular expressions [PSY_ECHOS_TICKS_INCLUDE]

-x, --stop

   Stop running tests after the first error or failure

-P, --no-path-adjustment

   Don't make any changes to sys.path when loading tests [PSY_ECHOS_TICKS_NOPATH]

--exe

   Look for tests in python modules that are executable. Normal
   behavior is to exclude executable modules, since they may not be
   import-safe [PSY_ECHOS_TICKS_INCLUDE_EXE]

--noexe

   DO NOT look for tests in python modules that are executable. (The
   default on the windows platform is to do so.)

--traverse-namespace

   Traverse through all path entries of a namespace package

--first-package-wins, --first-pkg-wins, --1st-pkg-wins

   psychoacoustics's importer will normally evict a package from sys.modules if
   it sees a package with the same name in a different location. Set
   this option to disable that behavior.

--no-byte-compile

   Prevent psychoacoustics from byte-compiling the source into .pyc files while
   psychoacoustics is scanning for and running tests.

-a=ATTR, --attr=ATTR

   Run only tests that have attributes specified by ATTR [PSY_ECHOS_TICKS_ATTR]

-A=EXPR, --eval-attr=EXPR

   Run only tests for whose attributes the Python expression EXPR
   evaluates to True [PSY_ECHOS_TICKS_EVAL_ATTR]

-s, --nocapture

   Don't capture stdout (any stdout output will be printed
   immediately) [PSY_ECHOS_TICKS_NOCAPTURE]

--nologcapture

   Disable logging capture plugin. Logging configuration will be left
   intact. [PSY_ECHOS_TICKS_NOLOGCAPTURE]

--logging-format=FORMAT

   Specify custom format to print statements. Uses the same format as
   used by standard logging handlers. [PSY_ECHOS_TICKS_LOGFORMAT]

--logging-datefmt=FORMAT

   Specify custom date/time format to print statements. Uses the same
   format as used by standard logging handlers. [PSY_ECHOS_TICKS_LOGDATEFMT]

--logging-filter=FILTER

   Specify which statements to filter in/out. By default, everything
   is captured. If the output is too verpsychoacoustics, use this option to
   filter out needless output. Example: filter=foo will capture
   statements issued ONLY to  foo or foo.what.ever.sub but not foobar
   or other logger. Specify multiple loggers with comma:
   filter=foo,bar,baz. If any logger name is prefixed with a minus, eg
   filter=-foo, it will be excluded rather than included. Default:
   exclude logging messages from psychoacoustics itself (-psychoacoustics). [PSY_ECHOS_TICKS_LOGFILTER]

--logging-clear-handlers

   Clear all other logging handlers

--logging-level=DEFAULT

   Set the log level to capture

--with-coverage

   Enable plugin Coverage:  Activate a coverage report using Ned
   Batchelder's coverage module.  [PSY_ECHOS_TICKS_WITH_COVERAGE]

--cover-package=PACKAGE

   Restrict coverage output to selected packages [PSY_ECHOS_TICKS_COVER_PACKAGE]

--cover-erase

   Erase previously collected coverage statistics before run

--cover-tests

   Include test modules in coverage report [PSY_ECHOS_TICKS_COVER_TESTS]

--cover-min-percentage=DEFAULT

   Minimum percentage of coverage for tests to pass
   [PSY_ECHOS_TICKS_COVER_MIN_PERCENTAGE]

--cover-inclusive

   Include all python files under working directory in coverage
   report.  Useful for discovering holes in test coverage if not all
   files are imported by the test suite. [PSY_ECHOS_TICKS_COVER_INCLUSIVE]

--cover-html

   Produce HTML coverage information

--cover-html-dir=DIR

   Produce HTML coverage information in dir

--cover-branches

   Include branch coverage in coverage report [PSY_ECHOS_TICKS_COVER_BRANCHES]

--cover-xml

   Produce XML coverage information

--cover-xml-file=FILE

   Produce XML coverage information in file

--cover-config-file=DEFAULT

   Location of coverage config file [PSY_ECHOS_TICKS_COVER_CONFIG_FILE]

--cover-no-print

   Suppress printing of coverage information

--pdb

   Drop into debugger on failures or errors

--pdb-failures

   Drop into debugger on failures

--pdb-errors

   Drop into debugger on errors

--no-deprecated

   Disable special handling of DeprecatedTest exceptions.

--with-doctest

   Enable plugin Doctest:  Activate doctest plugin to find and run
   doctests in non-test modules.  [PSY_ECHOS_TICKS_WITH_DOCTEST]

--doctest-tests

   Also look for doctests in test modules. Note that classes, methods
   and functions should have either doctests or non-doctest tests, not
   both. [PSY_ECHOS_TICKS_DOCTEST_TESTS]

--doctest-extension=EXT

   Also look for doctests in files with this extension
   [PSY_ECHOS_TICKS_DOCTEST_EXTENSION]

--doctest-result-variable=VAR

   Change the variable name set to the result of the last interpreter
   command from the default '_'. Can be used to avoid conflicts with
   the _() function used for text translation.
   [PSY_ECHOS_TICKS_DOCTEST_RESULT_VAR]

--doctest-fixtures=SUFFIX

   Find fixtures for a doctest file in module with this name appended
   to the base name of the doctest file

--doctest-options=OPTIONS

   Specify options to pass to doctest. Eg.
   '+ELLIPSIS,+NORMALIZE_WHITESPACE'

--with-isolation

   Enable plugin IsolationPlugin:  Activate the isolation plugin to
   isolate changes to external modules to a single test module or
   package. The isolation plugin resets the contents of sys.modules
   after each test module or package runs to its state before the
   test. PLEASE NOTE that this plugin should not be used with the
   coverage plugin, or in any other case where module reloading may
   produce undesirable side-effects.  [PSY_ECHOS_TICKS_WITH_ISOLATION]

-d, --detailed-errors, --failure-detail

   Add detail to error output by attempting to evaluate failed asserts
   [PSY_ECHOS_TICKS_DETAILED_ERRORS]

--with-profile

   Enable plugin Profile:  Use this plugin to run tests using the
   hotshot profiler.   [PSY_ECHOS_TICKS_WITH_PROFILE]

--profile-sort=SORT

   Set sort order for profiler output

--profile-stats-file=FILE

   Profiler stats file; default is a new temp file on each run

--profile-restrict=RESTRICT

   Restrict profiler output. See help for pstats.Stats for details

--no-skip

   Disable special handling of SkipTest exceptions.

--with-id

   Enable plugin TestId:  Activate to add a test id (like #1) to each
   test name output. Activate with --failed to rerun failing tests
   only.  [PSY_ECHOS_TICKS_WITH_ID]

--id-file=FILE

   Store test ids found in test runs in this file. Default is the file
   .psychoacousticsids in the working directory.

--failed

   Run the tests that failed in the last test run.

--processes=NUM

   Spread test run among this many processes. Set a number equal to
   the number of processors or cores in your machine for best results.
   Pass a negative number to have the number of processes
   automatically set to the number of cores. Passing 0 means to
   disable parallel testing. Default is 0 unless PSY_ECHOS_TICKS_PROCESSES is
   set. [PSY_ECHOS_TICKS_PROCESSES]

--process-timeout=SECONDS

   Set timeout for return of results from each test runner process.
   Default is 10. [PSY_ECHOS_TICKS_PROCESS_TIMEOUT]

--process-restartworker

   If set, will restart each worker process once their tests are done,
   this helps control memory leaks from killing the system.
   [PSY_ECHOS_TICKS_PROCESS_RESTARTWORKER]

--with-xunit

   Enable plugin Xunit: This plugin provides test results in the
   standard XUnit XML format. [PSY_ECHOS_TICKS_WITH_XUNIT]

--xunit-file=FILE

   Path to xml file to store the xunit report in. Default is
   psytests.xml in the working directory [PSY_ECHOS_TICKS_XUNIT_FILE]

--xunit-testsuite-name=PACKAGE

   Name of the testsuite in the xunit xml, generated by plugin.
   Default test suite name is psytests.

--xunit-prefix-with-testsuite-name

   Enables prefixing of the test class name in the xunit xml.
   This can be used in a matrixed build to distinguish between failures
   in different environments.
   If enabled, the testsuite name is used as a prefix.
   [PSY_ECHOS_TICKS_XUNIT_PREFIX_WITH_TESTSUITE_NAME]

--all-modules

   Enable plugin AllModules: Collect tests from all python modules.
   [PSY_ECHOS_TICKS_ALL_MODULES]

--collect-only

   Enable collect-only:  Collect and output test names only, don't run
   any tests.  [COLLECT_ONLY]
