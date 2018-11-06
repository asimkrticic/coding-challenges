# -*- coding: utf-8 -*-
import pandas as pd
import json
import os

__author__ = "Asim Krticic"


class Extract(object):
    """This class sets
     """
    @staticmethod 
    def extract_from_files(user_path=None,event_path=None):
        """
            Accepts paths to data source files.
            Reads two different data sources provided in .csv and .jsonl format.
            Returns two Pandas data frames - users and events.

            :param user_path: path to user data
            :param event_path: path to event data
            :type user_path: string
            :type event_path: string
            :returns: pandas data frames
            :rtype: data frame

        """

        try:

            # if paths not passed, take provided files 
            if event_path is None:
                event_path = 'events.jsonl'
            if user_path is None:
                user_path = 'users.csv'
            
            # create absolute path
            if not os.path.isabs(event_path):
                event_path = os.path.abspath(event_path)
            if not os.path.isabs(user_path):
                user_path = os.path.abspath(user_path)

        except IndexError:
            pass

        data = []
        with open(event_path) as f:
            for line in f:
                ob = json.loads(line)
                # add missing attributes
                if 'user_id' not in ob:
                    ob['user_id'] = pd.np.nan
                if 'tracking_id' not in ob:
                    ob['tracking_id'] = pd.np.nan
                if 'utm_medium' not in ob:
                    ob['utm_medium'] =   pd.np.nan#None
                if 'utm_campaign' not in ob:
                    ob['utm_campaign'] =  pd.np.nan#None
                    
                data.append(ob)

        # create data frames
        df_users = pd.DataFrame(data)
        df_events = pd.read_csv(user_path, delimiter=',')

        return df_users,df_events

