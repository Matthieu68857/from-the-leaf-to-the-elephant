from pymongo import MongoClient
from bson.json_util import dumps
from enum import Enum
import json
import functools
import time
import psycopg
from urllib.parse import urlparse

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        for key, value in kwargs.items():
            if key == "backend":
                print(f"{value.value} - {func.__name__} -  Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

class Backend(Enum):
    ATLAS = "Atlas"
    ATLAS_DURABILITY = "Atlas with Durability"
    FERRETDB = "FerretDB"
    POSTGRES = "PostgreSQL"

client_ferret = MongoClient("")
client_atlas = MongoClient("/?w=1&journal=false")
client_atlas_durability = MongoClient("/?w=majority&journal=true")
client_postgres = psycopg.connect("")
cursor = client_postgres.cursor()

@timer
def loop_insert_documents(client:MongoClient, backend:Backend):
    nb_of_documents = 0
    with open("fake_user_documents.json") as infile:
        for line in infile:
            if backend == Backend.POSTGRES:
                cursor.execute("INSERT INTO benchmark.users VALUES (%s)", (line,))
            else:
                client['ferretdb']['users'].insert_one(json.loads(line))
            nb_of_documents = nb_of_documents + 1
            if nb_of_documents % 1000 == 0:
                print(nb_of_documents)
            if nb_of_documents >= 10000:
                break

@timer
def delete_all(client:MongoClient, backend:Backend):
    #  client['ferretdb']['nobels'].delete_many({})
    if backend == Backend.POSTGRES:
        cursor.execute("TRUNCATE benchmark.users")
    else:
        client['ferretdb']['users'].drop()

@timer
def create_compound_index(client:MongoClient, backend:Backend):
    client['ferretdb']['nobels'].create_index([("surname", 1), ("firstname", 1)])
                                
@timer
def get_single_document(client:MongoClient, backend:Backend):
    client['ferretdb']['nobels'].find_one({ "firstname":"Pierre", "surname":"Curie"})

clients = [
    { "session": client_ferret, "backend": Backend.FERRETDB}, 
    { "session": client_atlas, "backend": Backend.ATLAS},
    { "session": client_atlas_durability, "backend": Backend.ATLAS_DURABILITY}
    { "session": client_postgres, "backend": Backend.POSTGRES}
]

for client in clients:
    delete_all(client=client["session"], backend=client["backend"])
    loop_insert_documents(client=client["session"], backend=client["backend"])
    # get_single_document(client=client["session"], backend=client["backend"])
    # create_compound_index(client=client["session"], backend=client["backend"])
    # get_single_document(client=client["session"], backend=client["backend"])

client_postgres.commit()
cursor.close()