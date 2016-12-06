#! /usr/bin/env python
import unittest
from profiler_builder import *

class Test(unittest.TestCase):
  def test_extractArguments(self):
    df, outputfile = extractArguments()

    self.assertEqual(seq, [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()