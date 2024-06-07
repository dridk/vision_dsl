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


def create_fake_data_for_domain(domain):
    # nécessite de choisir des keys-values en fonction des domaines (bio, pmsi, pharma)
    if domain == "bio":
        code = choice(["Fer","Glycemie", "Plaquettes", "Leucocytes", "Sodium", "Urée", "Vitamine D"])
    if domain == "pmsi" : 
        code = choice(["C000", "N99", "S031", "Z017", "E342", "B666", "F430", "C320", "E435", "D329"])
    if domain == "pharma":
        code = choice(["HBQK001", "HBQK002", "HBQH001", "HBQH002", "JCCP001", "JCCP002", "JCCP004"])
    return {"key" : code, "value": choice(range(0,200))}


def create_fake_data():
    user_df = pl.DataFrame([{"ipp":i, "age": choice(range(10,80)), "sex":choice([0,1])} for i in range(1000)])
    doc_df= pl.DataFrame([ {"ipp": choice(range(1000)), 
                            "text": " ".join(fake.text() for _ in range(50)) }
                            for _ in range(1000)   
                         ])
    data_df = pl.DataFrame([{"ipp":choice(range(1000)), "domain":choice(["bio", "pmsi", "pharma"])}for i in range(1000)])
    
    # ajout des keys-values en fonction du domaine
    code = [create_fake_data_for_domain(x) for x in data_df["domain"]]
    data_df = data_df.with_columns(
        pl.Series("key", [code["key"] for code in code]),
        pl.Series("value", [code["value"] for code in code])
    )
    return user_df, doc_df, data_df 


def create_sql_tables(conn):
    user_df, doc_df, data_df = create_fake_data()
    conn.sql("CREATE TABLE patients AS SELECT * FROM user_df")
    conn.sql("CREATE TABLE docs AS SELECT * FROM doc_df")
    conn.sql("CREATE TABLE data AS SELECT * FROM data_df")
    return conn


def main():
    conn = connection("vision.db")
    conn = create_sql_tables(conn)    
    return conn.close()



### RUN 
if __name__ == "__main__":
    main()




