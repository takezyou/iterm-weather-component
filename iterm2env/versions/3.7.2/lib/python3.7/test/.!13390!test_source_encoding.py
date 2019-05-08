# -*- coding: koi8-r -*-

import unittest
from test.support import TESTFN, unlink, unload, rmtree, script_helper, captured_stdout
import importlib
import os
import sys
import subprocess
import tempfile

class MiscSourceEncodingTest(unittest.TestCase):

    def test_pep263(self):
        self.assertEqual(
