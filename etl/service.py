# -*- coding: utf-8 -*-
import pandas as pd

__author__ = "Asim Krticic"


class Service(object):
    """This class
     """

    def __calculate_subscription_period(self, x):
        """
            Accepts joined data frame.
            Calculate subscription period for every user.
            Returns updated Pandas data frames with subscription period.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """ 
        # user have start and cancel subscription events, so we can use both to calculate period
        if x['_merge'] == 'both':
            x['subscription_year'] = int(abs(x['year_cancel']-x['year_start']))
            x['subscription_month'] = int(
                abs(x['month_cancel']-x['month_start']))
            x['subscription'] = str(
                int(x['subscription_year'])*12 + int(x['subscription_month'])) + ' months'
        # user only have start subscription events, so we use current date for cancel event in order to calculate period         
        elif x['_merge'] == 'left_only':
            x['subscription_year'] = abs(
                pd.to_datetime('today').year-x['year_start'])
            x['subscription_month'] = abs(pd.to_datetime(
                'today').month-x['month_start'])
            x['subscription'] = str(
                int(x['subscription_year'])*12 + int(x['subscription_month'])) + ' months'
        return x

    def customer_subscriptions(self, df,utm_medium=None,utm_campaign=None):
        """
            Accepts warehouse data frame and optional paramaters - utm_medium and utm_campaign.
            Calculate subscription period for every user.
            Returns filtred Pandas data frames with subscription period.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """      
        # Filtering conditions
        cond1 = df["type"] == 'Subscription Started'
        cond2 = df["type"] == 'Subscription Cancelled'  
        # If additional filtering params are passed
        if utm_medium is None and utm_campaign is None:
            cond_started = (cond1)
            cond_cancelled = (cond2)
        elif utm_medium is not None and utm_campaign is None:
            cond3 = df["utm_medium"] == utm_medium
            cond_started = (cond1 & cond3)
            cond_cancelled = (cond2 & cond3)
        elif utm_medium is None and utm_campaign is not None:
            cond3 = df["utm_campaign"]==utm_campaign
            cond_started = (cond1 & cond3)
            cond_cancelled = (cond2 & cond3)     
        elif utm_medium is not None and utm_campaign is not None:
            cond3 = df["utm_medium"]==utm_medium
            cond4 = df["utm_campaign"]==utm_campaign
            cond_started = (cond1 & (cond3 & cond4))
            cond_cancelled = (cond2 & (cond3 & cond4))
        # Filtered data from warehouse into two dataframes by Subscription Started and Subscription Cancelled event types
        subscription_started = df[cond_started]
        subscription_cancelled = df[cond_cancelled]
        # Outer Join these data frames in order to calculate subcription period
        subscribed_df = pd.merge(subscription_started, subscription_cancelled,
                                 how='outer', on='user_id', suffixes=('_start', '_cancel'), indicator=True)
        
        # Calculate subcription period
        subscribed_df = subscribed_df.apply(
            lambda row: self.__calculate_subscription_period(row), axis=1)

        # return empty data frame if no info about subscription,otherwise return data frame with calculated subscription period
        if len(subscribed_df)>0:
            return subscribed_df[['user_id', 'subscription']]
        else: 
            return pd.DataFrame(columns=['user_id','subscription']) 
        #return subscribed_df[['user_id', 'subscription','utm_medium_start']].groupby(['user_id', 'subscription','utm_medium_start']).size().reset_index(name='counts')

    def non_trial_customer(self, df,utm_medium=None,utm_campaign=None):
        """
            Accepts warehouse data frame and optional paramaters - utm_medium and utm_campaign.
            Count Users with either Signup Completed or Subscription Started event type.
            Returns filtred Pandas data frames with subscription period.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """  
        # Filtering conditions
        cond1 = df["type"] == 'Signup Completed'
        cond2 = df["type"] == 'Subscription Started'
        # If additional filtering params are passed
        if utm_medium is None and utm_campaign is None:
            cond = (cond1 | cond2)
        elif utm_medium is not None and utm_campaign is None:
            cond3 = df["utm_medium"] == utm_medium
            cond = ((cond1 | cond2) & (cond3))
        elif utm_medium is None and utm_campaign is not None:
            cond3 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3))        
        elif utm_medium is not None and utm_campaign is not None:
            cond3 = df["utm_medium"]==utm_medium
            cond4 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3 & cond4))
        temp = df[cond].groupby(
            ['user_id']).size().reset_index(name='counts')
        
        return len(temp)

    def from_trial_to_paid(self, df,utm_medium=None,utm_campaign=None):
        """
            Accepts warehouse data frame and optional paramaters - utm_medium and utm_campaign.
            Count Users with Trial Started and Subscription Started event type.
            Returns filtered Pandas dataframes grouped by year and month.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """ 
        # Filtering conditions
        cond1 = df["type"] == 'Trial Started'
        cond2 = df["type"] == 'Subscription Started'
        # If additional filtering params are passed
        if utm_medium is None and utm_campaign is None:
            cond = (cond1 | cond2)
        elif utm_medium is not None and utm_campaign is None:
            cond3 = df["utm_medium"] == utm_medium
            cond = ((cond1 | cond2) & (cond3))
        elif utm_medium is None and utm_campaign is not None:
            cond3 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3))        
        elif utm_medium is not None and utm_campaign is not None:
            cond3 = df["utm_medium"]==utm_medium
            cond4 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3 & cond4))

        # Count users that meet conditions
        temp = df[cond].groupby(
            ['user_id']).size().reset_index(name='counts')
        # Take only users that meet both conditions
        user_ids = list(temp[temp['counts'] >= 2]['user_id'])
        return df[(df['user_id'].isin(user_ids)) & (df['type'] == 'Subscription Started')].groupby(['year', 'month']).size().reset_index(name='counts')

    def customer_churn(self, df,utm_medium=None,utm_campaign=None):
        """
            Accepts warehouse data frame and optional paramaters - utm_medium and utm_campaign.
            Count Users with Subscription Started and Subscription Cancelled event type.
            Returns filtered Pandas dataframes grouped by year and month.

            :param df: warehouse data frame
            :type df: data frame
            :returns: pandas data frames
            :rtype: data frame

        """ 
        # Filtering conditions
        cond1 = df["type"] == 'Subscription Started'
        cond2 = df["type"] == 'Subscription Cancelled'

        # If additional filtering params are passed
        if utm_medium is None and utm_campaign is None:
            cond = (cond1 | cond2)
        elif utm_medium is not None and utm_campaign is None:
            cond3 = df["utm_medium"] == utm_medium
            cond = ((cond1 | cond2) & (cond3))
        elif utm_medium is None and utm_campaign is not None:
            cond3 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3))        
        elif utm_medium is not None and utm_campaign is not None:
            cond3 = df["utm_medium"]==utm_medium
            cond4 = df["utm_campaign"]==utm_campaign
            cond = ((cond1 | cond2) & (cond3 & cond4))

        # Count users that meet conditions
        temp = df[cond].groupby(
            ['user_id']).size().reset_index(name='counts')
        # Take only users that meet all conditions
        user_ids = list(temp[temp['counts'] >= 2]['user_id'])
        return df[(df['user_id'].isin(user_ids)) & (df['type'] == 'Subscription Cancelled')].groupby(['year', 'month']).size().reset_index(name='counts')
