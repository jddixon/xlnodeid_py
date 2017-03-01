# xlnodeid/__init__.py

""" NodeID library for python XLattice packages. """

__version__ = '0.0.2'
__version_date__ = '2017-03-01'

__all__ = ['__version__', '__version_date__', 'XLNodeIDError', ]


class XLNodeIDError(RuntimeError):
    """ General purpose exception for the package. """
