# -*- coding: utf-8 -*-
import pandas as pd

__author__ = "Asim Krticic"


class Load(object):
    """This class sets
     """
    @staticmethod   
    def save_to_csv(df):
        """
            Accepts data frame - warehouse.
            Save data frame into csv file without indices.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """
        df.to_csv('warehouse.csv', sep=',', encoding='utf-8', index=False)

