import io
import os
import sys
from etl.extract import Extract
from etl.transform import Transform
from etl.load import Load
from service import Service
import pandas as pd

import math


if __name__ == "__main__":

    df_users,df_events=Extract.extract_from_files()
    combined_df=Transform.merge_dataframes(df_users,df_events)
    Load.save_to_csv(combined_df)
    
    service = Service()
    customer_subscriptions = service.customer_subscriptions(combined_df)
    non_trial_customer=service.non_trial_customer(combined_df)
    from_trial_to_paid=service.from_trial_to_paid(combined_df)
    customer_churn=service.customer_churn(combined_df)

    print "\nCustomer Subscriptions\n","----------------------\n" ,customer_subscriptions
    print "\nNon Trial Customer\n","----------------------\n" ,non_trial_customer
    print "\nFrom Trial To Paid\n","----------------------\n" ,from_trial_to_paid
    print "\nCustomer Churn\n","----------------------\n" ,customer_churn
