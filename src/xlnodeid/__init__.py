# xlnodeid/__init__.py

""" NodeID library for python XLattice packages. """

from binascii import b2a_hex
from copy import deepcopy

from xlattice import SHA1_BIN_LEN, SHA2_BIN_LEN, SHA3_BIN_LEN

__version__ = '0.0.6'
__version_date__ = '2017-05-29'

__all__ = ['__version__', '__version_date__',
           'XLNodeIDError', 'XLNodeID']


class XLNodeIDError(RuntimeError):
    """ General purpose exception for the package. """


class XLNodeID(object):
    """ Unique identifier for an XLattice Node. """

    def __init__(self, ident):
        if not ident:
            raise XLNodeIDError("id may not be None or empty")
        if not (isinstance(ident, bytes) or isinstance(ident, bytearray)):
            raise XLNodeIDError("NodeID value must be bytes-like")

        length = len(ident)
        if length != SHA1_BIN_LEN and length != SHA2_BIN_LEN and \
                length != SHA3_BIN_LEN:
            raise XLNodeIDError("invalid nodeID length %d" % length)

        # it's a valid ID, so deep copy it
        self._node_id = bytes(deepcopy(ident))

    @property
    def value(self):
        """ Return a deep copy of the underlying byte sequence. """

        return deepcopy(self._node_id)

    @staticmethod
    def is_valid_node_id(val):
        """ Return whether val is a valid XLNodeID value. """
        if not val:
            return False
        if not isinstance(val, bytes) and not isinstance(val, bytearray):
            return False

        length = len(val)
        if length != SHA1_BIN_LEN and length != SHA2_BIN_LEN and \
                length != SHA3_BIN_LEN:
            return False

        return True

    def clone(self):
        """ Return a deep copy of the XLNodeID instance. """
        return XLNodeID(self._node_id)

    def __eq__(self, other):
        if not isinstance(other, XLNodeID):
            return False
        return self._node_id == other.value

    def __lt__(self, other):
        return self._node_id < other.value

    def __str__(self):
        return b2a_hex(self._node_id)

    def __len__(self):
        return len(self._node_id)
