# load configuration

import sys
sys.path.append("../utils")
import wxd_utils

conf=wxd_utils.load_conf()
print(conf)

# connect to Presto / watsonx.data

wxd_engine = wxd_utils.connect_wxd(conf)

# delete table and schema

import sqlalchemy 

try:

    drop_table = "drop table iceberg_data.simple_rag.wikipedia"
    drop_schema = "drop schema iceberg_data.simple_rag"

    with wxd_engine.connect() as connection:
            connection.execute(drop_table)
            connection.execute(drop_schema)

    print("table wikipedia and schema simple_rag removed")

except sqlalchemy.exc.SQLAlchemyError as e:
    print("Error:", str(e))

# connect to Milvus

from pymilvus import(
    Milvus,
    IndexType,
    Status,
    connections,
    FieldSchema,
    DataType,
    Collection,
    CollectionSchema,
)

connections.connect(alias = 'default',
                host = conf["host"],
                port = conf["milvus_port"],
                user = conf["user"],
                password = conf["password"],
                server_pem_path = conf["lh_cert"],
                server_name = conf["host"],
                secure = True)

# remove collection

try: 

    basic_collection = Collection("wiki_articles") 
    basic_collection.drop()

    print("collection wiki_articles removed")
    
except Exception as e:
    print("Error:", str(e))

