#!/usr/bin/env python3
# xlnodeid_py/test_node_id.py

""" Verify that an XLNodeID behaves like one. """

import time
import unittest
from copy import deepcopy

from rnglib import SimpleRNG
from xlattice import SHA1_BIN_LEN, SHA2_BIN_LEN, SHA3_BIN_LEN
from xlnodeid import XLNodeID, XLNodeIDError


class TestNodeID(unittest.TestCase):
    """ Verify that an XLNodeID behaves like one. """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_valid_node_id(self):
        """
        Tests the funnction of that name.
        """

        # tests that should fail
        self.assertFalse(XLNodeID.is_valid_node_id(None))
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
        """ Expect object construction to fail. """
        try:
            _ = XLNodeID(val)
            self.fail("XLNodeID constructed with bad ID")
        except XLNodeIDError:
            pass

    def expect_success(self, val):
        """
        Try to build a NodeID with val (a bytes valaue).
        """
        try:
            nodeid = XLNodeID(val)
            # succeeded
        except XLNodeIDError:
            self.fail("ctor raised with good ID")

        val2 = nodeid.value
        self.assertIsNotNone(val2)
        self.assertFalse(val2 is val)   # not the same object
        self.assertEqual(val2, val)     # but a valid deep copy

    def test_ctor(self):
        """
        Tests the XLNodeID constructor.
        """

        # tests that should fail
        self.expect_failure(None)    # id may not be None
        self.expect_failure('foo')   # not bytes-like
        self.expect_failure(b'bar')  # wrong length
        self.expect_failure(42)      # an int

        self.expect_failure(bytes(SHA1_BIN_LEN - 1))
        self.expect_failure(bytes(SHA1_BIN_LEN + 1))
        self.expect_failure(bytes(SHA2_BIN_LEN - 1))
        self.expect_failure(bytes(SHA2_BIN_LEN + 1))
        self.expect_failure(bytes(SHA3_BIN_LEN - 1))
        self.expect_failure(bytes(SHA3_BIN_LEN + 1))

        # tests that should succeed
        val = self.rng.some_bytes(SHA1_BIN_LEN)
        self.expect_success(val)
        val = self.rng.some_bytes(SHA2_BIN_LEN)
        self.expect_success(val)
        val = self.rng.some_bytes(SHA3_BIN_LEN)
        self.expect_success(val)

    def do_test_cloning(self, length):
        """ Verify that cloning works for a given number of bytes. """
        val = self.rng.some_bytes(length)
        id1 = XLNodeID(val)
        id2 = id1.clone()
        self.assertTrue(id1 is not id2)
        self.assertEqual(id1.value, id2.value)

    def test_cloning(self):
        """ Test cloning for bytes-like objects of a given number of bytes. """
        for length in [SHA1_BIN_LEN, SHA2_BIN_LEN, SHA3_BIN_LEN]:
            self.do_test_cloning(length)

    def do_test_comparison(self, length):
        """
        For a quasi-random byte sequence of a given length, verify that
        comparison opertors work.
        """
        val = self.rng.some_bytes(length)       # a byte array of that length

        # pick a random index into that byte array
        ndx = 1 + self.rng.next_int16(length - 1)
        if val[ndx] == 0:
            val[ndx] = 1
        if val[ndx] == 255:
            val[ndx] = 254

        # make a couple of clones of the byte array
        v_bigger = deepcopy(val)
        v_bigger[ndx] += 1
        v_smaller = deepcopy(val)
        v_smaller[ndx] -= 1

        self.assertTrue(v_bigger > val)
        self.assertTrue(v_smaller < val)

        # use these values to make NodeIDs
        n_bigger = XLNodeID(v_bigger)
        n_middle = XLNodeID(val)
        n_smaller = XLNodeID(v_smaller)

        # compare them
        self.assertTrue(n_bigger > n_middle)
        self.assertTrue(n_smaller < n_middle)

        # equality checks
        self.assertEqual(n_middle, n_middle)
        self.assertFalse(n_bigger == n_middle)
        self.assertFalse(n_middle == n_smaller)

    def test_comparion(self):
        """ Test comparison operators for IDs of standard lengths. """
        for length in [SHA1_BIN_LEN, SHA2_BIN_LEN, SHA3_BIN_LEN]:
            self.do_test_comparison(length)


if __name__ == '__main__':
    unittest.main()
