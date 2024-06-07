import duckdb 
import os
import polars as pl
from random import choice
# pip install Faker
from faker import Faker
fake = Faker()


def connection(database):
    if os.path.exists(database):
        os.remove(database)
    conn = duckdb.connect(database)
    return conn


def create_fake_data():
    user_df = pl.DataFrame([{"ipp":i, "age": choice(range(10,80)), "sex":choice([0,1])} for i in range(1000)])
    doc_df= pl.DataFrame([ {"ipp": choice(range(1000)), 
                            "text": fake.text() }
                            for _ in range(1000)   
                         ])
    data_df = pl.DataFrame([{"ipp":choice(range(1000)), "domain":"bio", "code":choice(["Fer","Glycemie"]),"value": choice(range(0,10))} for i in range(1000)])
    return user_df, doc_df, data_df

def create_sql_tables(conn):
    conn.sql("CREATE TABLE patients AS SELECT * FROM user_df")
    conn.sql("CREATE TABLE docs AS SELECT * FROM doc_df")
    conn.sql("CREATE TABLE data AS SELECT * FROM data_df")
    return conn

def table_viewer(conn):
    for table_name in ["patients", "docs", "data"]:
        print(conn.sql(f"SELECT * FROM {table_name} LIMIT 10"))

    
def main():
    conn = connection("vision.db")
    user_df, doc_df, data_df = create_fake_data()
    conn = create_sql_tables(conn)
    table_viewer(conn)
    
    conn.close()



### RUN 
if __name__ == "__main__":
    main()
