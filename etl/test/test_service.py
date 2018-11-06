# -*- coding: utf-8 -*-
import shutil
import tempfile
import unittest
import io
import os
import sys
from StringIO import StringIO
from service import Service
import pandas as pd

__author__ = "Asim Krticic"


class TestServiceFunctions(unittest.TestCase):
    """
    This class contains sanity test cases for Service class methods
    The results returned from the methods are inner joined with
    the expected results. The test will pass if the number of
    rows and columns, and data are matching.

    """

    def setUp(self):
        """
        Set up test warehouse
        """
        self.warehouse = StringIO("""type,utm_campaign,utm_medium,month,year,email,user_id
        Trial Started,None,None,1,2017,,c0b3334e-fec9-4805-aadd-7efbe053a515
        Subscription Started,None,None,2,2017,,c0b3334e-fec9-4805-aadd-7efbe053a515
        Subscription Cancelled,None,None,3,2017,,c0b3334e-fec9-4805-aadd-7efbe053a515
        Subscription Started,None,None,5,2017,,53d2c7e4-605f-41c2-a6c3-6778a3642b02
        Subscription Cancelled,None,None,6,2017,,53d2c7e4-605f-41c2-a6c3-6778a3642b02
        Signup Completed,None,None,2,2017,richsara@yahoo.com,4c683546-7ec0-4274-ace7-b318ef723278
        Signup Completed,None,None,2,2017,brettmiller@dunlap.com,8be6a1cc-06cd-4190-8355-e1dc269beb98
        Signup Completed,None,None,2,2017,eavila@yahoo.com,8dc6a5db-efb3-4ecc-93da-84f0414acc9a
        Signup Completed,audio,google,4,2017,thompsonkeith@lewis-ford.org,c63477ff-6b73-42b8-9d53-8bf3356b0719
        Trial Started,None,None,4,2017,,c63477ff-6b73-42b8-9d53-8bf3356b0719
        Subscription Started,None,None,4,2017,,c63477ff-6b73-42b8-9d53-8bf3356b0719
        Subscription Cancelled,None,None,5,2017,,c63477ff-6b73-42b8-9d53-8bf3356b0719
        """)

        self.df_warehouse = pd.read_csv(self.warehouse, delimiter=',')
        self.df_warehouse['type'] = self.df_warehouse['type'].str.strip()

    def test_subscription(self):
        test_data = [{'user_id': 'c0b3334e-fec9-4805-aadd-7efbe053a515', 'subscription': '1 months'},
                     {'user_id': 'c63477ff-6b73-42b8-9d53-8bf3356b0719',
                      'subscription': '1 months'},
                     {'user_id': '53d2c7e4-605f-41c2-a6c3-6778a3642b02',
                      'subscription': '1 months'},
                     ]
        df_test = pd.DataFrame(test_data)

        df = Service().customer_subscriptions(self.df_warehouse)

        result = pd.merge(
            df_test, df, on=['user_id', 'subscription'], how='inner')
        self.assertEqual(len(df), len(result))

    def test_non_trial_customer(self):
        result = Service().non_trial_customer(self.df_warehouse)
        self.assertEqual(result, 6)

    def test_non_trial_customer_medium(self):
        result = Service().non_trial_customer(self.df_warehouse, 'google')
        self.assertEqual(result, 1)

    def test_non_trial_customer_campaign(self):
        result = Service().non_trial_customer(self.df_warehouse, None, 'audio')
        self.assertEqual(result, 1)

    def test_from_trial_to_paid(self):
        test_data = [{'year': 2017, 'month': 2, 'counts': 1},
                     {'year': 2017, 'month': 4, 'counts': 1}]
        df_test = pd.DataFrame(test_data)
        df = Service().from_trial_to_paid(self.df_warehouse)
        result = pd.merge(
            df_test, df, on=['year', 'month', 'counts'], how='inner')
        self.assertEqual(len(df), len(result))

    def test_customer_churn(self):
        test_data = [{'year': 2017, 'month': 3, 'counts': 1},
                     {'year': 2017, 'month': 5, 'counts': 1},
                     {'year': 2017, 'month': 6, 'counts': 1}, ]

        df_test = pd.DataFrame(test_data)
        df = Service().customer_churn(self.df_warehouse)
        result = pd.merge(
            df_test, df, on=['year', 'month', 'counts'], how='inner')
        self.assertEqual(len(df), len(result))


if __name__ == '__main__':
    unittest.main()
