# -*- coding: utf-8 -*-

__author__ = "Asim Krticic"

class Item(object):
    """Base class for items """

    def __init__(self, index=-1, weight=0, cost=0):
        self._index = index
        self._weight = weight
        self._cost = cost

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value


class Package(Item):
    """This class sets the package limit and handles adding of items
        to the item's list
     """

    def __init__(self, package_limit=-1):
        self._package_limit = package_limit
        self._items = []

    @property
    def items(self):
        return self._items

    def add_item(self, index=-1, weight=0, cost=0):
        it = Item(index, weight, cost)
        self._items.append(it)
