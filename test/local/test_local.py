from numpy import arange, ones, repeat

from bolt import array
from bolt.spark.array import BoltArraySpark
from bolt.utils import allclose

import generic

def test_construct():
    x = arange(2*3*4).reshape((2, 3, 4))
    b = array(x)
    assert b.shape == (2, 3, 4)


def test_toarray():

    x = arange(2*3*4).reshape((2, 3, 4))
    b = array(x)
    assert allclose(b.toarray(), x)

def test_tospark(sc):

    x = arange(2*3*4).reshape((2, 3, 4))
    b = array(x)
    s = b.tospark(sc, axes=(0,))
    assert isinstance(s, BoltArraySpark)
    assert s.shape == (2, 3, 4)
    assert allclose(s.toarray(), x)

def test_tordd(sc):

    from pyspark import RDD
    x = arange(2*3*4).reshape((2, 3, 4))

    b = array(x)
    r = b.tordd(sc, axes=(0,))
    assert isinstance(r, RDD)
    assert r.count() == 2

    r = b.tordd(sc, axes=(0, 1))
    assert isinstance(r, RDD)
    assert r.count() == 2*3

    r = b.tordd(sc, axes=(0, 1, 2))
    assert isinstance(r, RDD)
    assert r.count() == 2*3*4

"""
Testing functional operators
"""

def test_map():

    import random
    random.seed(42)

    x = arange(2*3*4).reshape(2, 3, 4)
    b = array(x)

    # Test all generic map functionality
    generic.map_suite(x, b)


def test_reduce():

    from numpy import asarray

    dims = (10, 10, 10)
    area = dims[0] * dims[1]
    arr = asarray([repeat(x,area).reshape(dims[0], dims[1]) for x in range(dims[2])])
    b = array(arr)

    # Test all generic reduce functionality
    generic.reduce_suite(arr, b)


def test_filter():

    x = arange(2*3*4).reshape(2, 3, 4)
    b = array(x)

    # Test all generic filter functionality
    generic.filter_suite(x, b)
