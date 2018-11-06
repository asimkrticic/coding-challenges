# -*- coding: utf-8 -*-
import shutil
import tempfile
import unittest
import io
import os
import sys
from package.packer import Packer
from package.exception import APIException

__author__ = "Asim Krticic"

class TestPackerFunctions(unittest.TestCase):
    """This class contains basic test cases for Packer class method pack()"""

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.path = os.path.join(self.test_dir, 'test.txt')

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_no_path(self):
        with self.assertRaises(APIException) as cm:
            Packer.pack(None)
        self.assertTrue(
            'A valid file path expected as an argument!' in cm.exception)

    def test_relative_path(self):
        with self.assertRaises(APIException) as cm:
            Packer.pack('input_file/test_inputs.txt')
        self.assertTrue(
            'You need to provide an absolute path to a file!' in cm.exception)

    def test_packing(self):
        f = open(self.path, 'w')
        f.write(
            "81 : (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48)")
        f = open(self.path, 'r')
        self.assertEqual(Packer.pack(self.path), '4')

    def test_weight_limit(self):
        f = open(self.path, 'w')
        f.write(
            "101 : (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48)")
        f = open(self.path, 'r')
        with self.assertRaises(APIException) as cm:
            Packer.pack(self.path)
        self.assertTrue(
            'Max weight that a package can take is <= 100!' in cm.exception)

    def test_item_limit(self):
        f = open(self.path, 'w')
        f.write("81 : (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48) (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48) (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48)")
        f = open(self.path, 'r')
        with self.assertRaises(APIException) as cm:
            Packer.pack(self.path)
        self.assertTrue(
            'Package can take max 15 items!' in cm.exception)

    def test_max_item_cost(self):
        f = open(self.path, 'w')
        f.write(
            "81 : (1,53.38,€101) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48)")
        f = open(self.path, 'r')
        with self.assertRaises(APIException) as cm:
            Packer.pack(self.path)
        self.assertTrue(
            'Max weight and cost of an item need to be ≤ 100!' in cm.exception)

    def test_max_item_weight(self):
        f = open(self.path, 'w')
        f.write(
            "81 : (1,101,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9) (6,46.34,€48)")
        f = open(self.path, 'r')
        with self.assertRaises(APIException) as cm:
            Packer.pack(self.path)
        self.assertTrue(
            'Max weight and cost of an item need to be ≤ 100!' in cm.exception)


if __name__ == '__main__':
    unittest.main()
