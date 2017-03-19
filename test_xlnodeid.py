#!/usr/bin/env python3
# xlnodeid_py/test_node_id.py

""" Verify that an XLNodeID behaves like one. """

#import hashlib
#import os
import time
import unittest

from rnglib import SimpleRNG
from xlattice import SHA1_BIN_LEN, SHA2_BIN_LEN, SHA3_BIN_LEN
from xlnodeid import XLNodeID, XLNodeIDError


class TestNodeID(unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_valid_node_id(self):
        """
        Tests the funnction of that name.
        """

        # tests that should fail
        self.assertFalse(XLNodeID.is_valid_node_id(None)
                         )   # id may not be None
        self.assertFalse(XLNodeID.is_valid_node_id('foo'))  # not bytes-like
        self.assertFalse(XLNodeID.is_valid_node_id(b'bar'))  # wrong length
        self.assertFalse(XLNodeID.is_valid_node_id(42))     # an int

        # tests that should succeed
        val = bytes(SHA1_BIN_LEN)
        self.assertTrue(XLNodeID.is_valid_node_id(val))
        val = bytes(SHA2_BIN_LEN)
        self.assertTrue(XLNodeID.is_valid_node_id(val))
        val = bytes(SHA3_BIN_LEN)
        self.assertTrue(XLNodeID.is_valid_node_id(val))

    def expect_failure(self, val):
        try:
            obj = XLNodeID(val)
            fail("XLNodeID constructed with bad ID")
        except XLNodeIDError:
            pass

    def expect_success(self, val):
        try:
            obj = XLNodeID(val)
            # succeeded
        except XLNodeIDError:
            self.fail("ctor raised with good ID")

    def test_ctor(self):
        """
        Tests the XLNodeID constructor.
        """

        # tests that should fail
        self.expect_failure(None)    # id may not be None
        self.expect_failure('foo')   # not bytes-like
        self.expect_failure(b'bar')  # wrong length
        self.expect_failure(42)      # an int

        # tests that should succeed
        val = bytes(SHA1_BIN_LEN)
        self.expect_success(val)
        val = bytes(SHA2_BIN_LEN)
        self.expect_success(val)
        val = bytes(SHA3_BIN_LEN)
        self.expect_success(val)


if __name__ == '__main__':
    unittest.main()
