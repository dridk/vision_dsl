import duckdb 
import os
import polars as pl
from random import choice
# pip install Faker
from faker import Faker

database_name = "vision.db"
if os.path.exists(database_name):
    os.remove(database_name)
    
conn = duckdb.connect(database_name)
fake = Faker()

## Create users 
user_df = pl.DataFrame([{"ipp":i, "age": choice(range(10,80)), "sex":choice([0,1])} for i in range(1000)])
doc_df= pl.DataFrame([ {"ipp": choice(range(1000)), 
                        "text": fake.text() }
                        for _ in range(1000)   
                     ])
data_df = pl.DataFrame([{"ipp":choice(range(1000)), "domain":"bio", "code":choice(["Fer","Glycemie"]),"value": choice(range(0,10))} for i in range(1000)])


conn.sql("CREATE TABLE patients AS SELECT * FROM user_df")
conn.sql("CREATE TABLE docs AS SELECT * FROM doc_df")
conn.sql("CREATE TABLE data AS SELECT * FROM data_df")
conn.close()