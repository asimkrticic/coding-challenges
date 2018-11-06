#  Data Engineering Challenge

Author: Asim Krticic

This submission is a response to coding challenge. The purpose was to create a simple ETL job that will take as input different data sources. The idea was to write the output to a SQL database or CSV files and to implement the requirements defined in the challenge that will return results on the data warehouse table which is product of the ETL.

To implement the program, I chose Python v2.7.10 and latest version of Pandas.


### Usage

To run the program in the project root please execute the following command:
```sh
$ 	python run.py
```

To run the unit tests please execute the following command:
```sh 
$   python -m unittest discover
```

### Approach

The project is structured following Python’s best practice.
Folder structure:
```bash
├── blendle-code-challenge
│   ├── etl
│   │   ├── __init__.py
│   │   ├── export.py
│   │   ├── transform.py
│   │   ├── load.py
│   ├── test
│   ├── ├── __init.py__
│   ├── ├── test_service.py
│   ├── docs
│   │   ├── **doc files**
├── run.py
├── service.py
├── README.md
├── requirements.txt
├── setup.py
```
The `__init__.py` files are required to make Python treat the directories as containing packages.

For the purposes of demonstration, the run.py file was created, which initiates ETL process and prints the results of the requirements defined in the challenge.

Using objective oriented approach, a certain information was grouped in classes Extract, Transform and Load for better maintainability and reusability of code.
The class Extract contains extract_from_files static method, which reads two different data sources provided in .csv and .jsonl format and returns two Pandas data frames - users and events.
The class Transform contains merge_dataframes static method. This method validates date format, adjusts data type and performs denormalization of data column into month and year. Furthermore, updates user_id column in event data frame based on user data frame using tracking_id as reference key. The method returns transformed and denormalized event data frame that represents data warehouse table.
The class Load contains save_to_csv static method, that stores the output of transform to CSV file, which is chosen as a simpler solution instead of storing to a database.

To implement the requirements defined in the challenge, the Service class was created which contains four methods and one private helper method:
- Customer_subscriptions method returns a list of user_ids with their period of subscription. For users that still haven’t cancelled their subscription, the current date was used as end of subscription period. Note: From the requirements in the challenge, it wasn’t clear if such cases should be even taken into consideration. However, this is the way I decided to include them.
- Non_trial_customer method returns a number of users that have Signup Completed or Subscription Started event type.
- From_trial_to_paid method returns a number of users that have both Trial Started and Subscription Started event type per year and month.
- Customer_churn method returns a number of users that have Subscription Started and Subscription Cancelled event type per year and month.
NOTE: The point five of the requirements in the challenge: “Each of the above, but divided by UTM source/campaign.” is implemented by adding additional arguments for utm_medium and utm_campain due to the lack of time. However, the implementation would be pretty much the same as all of the above with two additional columns in groupby.

The test directory contains unit tests. Tests are created in Python’s unittest framework. The TestServiceFunctions class contains sanity test cases for the four methods from Service class. To avoid dependency on test data stored in the files but still to test the methods by passing the data in csv format, a memory file is created in setup method before each test case.



Code was formatted using Python PEP8 coding style guide. Docstrings in methods and classes are ready for generating documentation using Sphinx.





