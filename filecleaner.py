#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 16:21:29 2019

@author: ashwinraghurajan
"""

# This script imports, analyzes, and cleans the legally_operating_business CSV file
# The process removes unnecessary columnsa and handles missing values
# The process further normalizes and returns a file to be later used to build the Flask API

import pandas as pd
import numpy as np
import sqlite3

# df = pd.read_csv('/Users/ashwinraghurajan/Documents/Py/datasets/Legally_Operating_Businesses.csv')
df1 = pd.read_csv('/Users/ashwinraghurajan/Documents/Py/datasets/Legally_Operating_Businesses.csv', 
                  sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
df1_head = df1.head()


# strip out the 'DCA' text portion to get a unique numerical identifier for the data
# return only licenses that are "active"
# drop columns that are unnecessary ()
# then takes in user coordinates and desired industry and locates nearest 
# business within that industry


# get an understanding of which columns exist and which ones to remove
columnlist = list(df1.columns)
lenlist = [i for i in range(len(columnlist))]
column_frame = pd.DataFrame({'names':columnlist, 'index':lenlist})

# drop unnecessary columns after viewing the dataframe head
drop_cols = np.r_[7:14,15:27]
df1.drop(df1.columns[drop_cols], axis=1, inplace=True)

# strip out the 'DCA' portion of the license numbers
# also check for unique values for license numbers
df1.iloc[:,0] = df1.iloc[:,0].map(lambda x: x.rstrip('-DCA'))

print(df1.iloc[:,0].agg(['nunique','count','size']))
print(df1.iloc[:,0].nunique() == df1.iloc[:,0].count())

# find the repeated values in the DCA license number column
duplicates = df1[df1.duplicated(['DCA License Number'],keep=False)]
print(duplicates)

# We notice that all the repeated values for this column are data points with inactive licenses
# and since we want to strip out inactive licenses anyways, these duplicated values will be ultimately deleted
# these next actions will remove rows with inactive licenses

df1 = df1[df1.iloc[:,3] != "Inactive"]

# change "nan" for businesses that do not have a contact phone number and put in something more user friendly and appropriate
df1['Contact Phone Number'].fillna("Not Available",inplace=True)


# standardize the phone number format
df1['Contact Phone Number'].str.replace("-","")

# change the column name headings to remove the space
df1.columns = ['license_number','license_type','license_expiration','license_status','license_creation_date',
               'industry','business_name','phone_number']

# export the cleaned dataframe to SQlite3 database which we will use later on
conn = sqlite3.connect('/Users/ashwinraghurajan/Documents/Py/api1/nycbusiness.db')
df1.to_sql('businesses', conn, if_exists='append', index=False)

 