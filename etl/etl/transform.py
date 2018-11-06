# -*- coding: utf-8 -*-
import pandas as pd

__author__ = "Asim Krticic"


class Transform(object):
    """This class sets
     """
    @staticmethod    
    def merge_dataframes(df,df2):
        """
            Accepts two data frames - users and events.
            Cleaning, formating, transforming and extracting new columns from two different data sources.
            Returns transformed Pandas data frame.

            :param df: users data frame
            :param df2: events data frame
            :type df: data frame
            :type df2: data frame
            :returns: pandas data frames
            :rtype: data frame

        """

        # convert to datetime format
        df['created_at'] = pd.to_datetime(df['created_at'],errors='coerce')
        # new columns
        df['month'] = df['created_at'].dt.month
        df['year'] = df['created_at'].dt.year
        #strip type column
        df['type'] = df['type'].str.strip()

        # set missing values
        mask_medium = df['utm_medium'].isnull()
        column_name = 'utm_medium'
        df.loc[mask_medium, column_name] = pd.np.nan
        
        mask_campaign= df['utm_campaign'].isnull()
        column_name = 'utm_campaign'
        df.loc[mask_campaign, column_name] = pd.np.nan

        # join users and events data frames by tracking_id
        combined_df = pd.merge(df, df2, how = 'outer', on= 'tracking_id', suffixes= ('_user', '_event'), indicator= True)
        # update user_id column in event data frame, from users frame
        combined_df['user_id'] = combined_df['user_id_user'].where(combined_df['user_id_event'].isnull(), combined_df['user_id_event'])

        # drop unnecessary columns
        columns = ['created_at','tracking_id','user_id_user','user_id_event','_merge']
        combined_df.drop(columns, inplace=True, axis=1)
        return combined_df

