#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 01:11:05 2019

@author: ashwinraghurajan
"""

import flask
from flask import request, jsonify
import sqlite3
import csv
import pandas as pd

# import the nyc_business.csv file created by filecleaner.py into SQLite3 Database to called upon by our API methods

conn = sqlite3.connect('/Users/ashwinraghurajan/Documents/Py/api1/nycbusinesses.db')
cursor = conn.cursor()

df = pd.read_csv('/Users/ashwinraghurajan/Documents/Py/api1/nyc_businesses.csv')
df.to_sql('businesses', conn, if_exists='append', index=False)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/', methods=['GET'])
def home():
    return '''<h1>NYC businesses based on your location</h1>
<p>An API I built so you can find helpful businesses in the City that are closest to you</p>'''

# return business_name, phone_number, license_type
# this method specifies all the different categories the user can input to get a list of businesses and their phone numbers
@app.route('/api/v1/resources/businesses/dictionary', methods=['GET'])
def api_dictionary():
    
    conn = sqlite3.connect('/Users/ashwinraghurajan/Documents/Py/api1/nycbusinesses.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = 'SELECT DISTINCT(industry) FROM businesses;'
    all_business_types = cur.execute(query).fetchall()
    
    return jsonify(all_business_types)


@app.route('/api/v1/resources/businesses', methods=['GET'])
def api_all():
    
    name = request.args.get('industry')
    query = "SELECT business_name, phone_number, license_type FROM businesses WHERE"
    param = []
    
    if name:
        query += ' industry=?;'
        param.append(name)
    if not name:
        return page_not_found(404)
    
    conn = sqlite3.connect('/Users/ashwinraghurajan/Documents/Py/api1/nycbusinesses.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    result = cur.execute(query,param).fetchall()
    
    return jsonify(result)

app.run()



    
        
    
    
    
    
    
    
    
    
    








