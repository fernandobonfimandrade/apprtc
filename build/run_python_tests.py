#!/usr/bin/python

import os
import optparse
import sys
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH     Path to the SDK installation.
TEST_PATH    Path to package containing test modules.
WEBTEST_PATH Path to the webtest library."""


def _WebTestIsInstalled():
  try:
    import webtest
    return True
  except ImportError:
    print 'You need to install webtest before you can proceed running the '
    print 'tests. To do this you need to get easy_install. See '
    print 'https://pythonhosted.org/setuptools/easy_install.html'
    print 'Then:'
    print 'cd webtest-master'
    print 'sudo python setup.py install'
    return False


def main(sdk_path, test_path, webtest_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    sys.path.append(webtest_path)
    if not _WebTestIsInstalled():
      return False
    suite = unittest.loader.TestLoader().discover(test_path,
                                                  pattern="*test.py")
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 3:
        print 'Error: Exactly 3 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    WEBTEST_PATH = args[2]
    sys.exit(not main(SDK_PATH, TEST_PATH, WEBTEST_PATH))
