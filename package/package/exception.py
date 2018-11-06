# -*- coding: utf-8 -*-
import sys

__author__ = "Asim Krticic"


class APIException(Exception):
    '''Raise APIException when there's a constraints error'''

    @staticmethod
    def exception_handler(exception_type, exception, traceback):
        print "%s: %s" % (exception_type.__name__, exception)
