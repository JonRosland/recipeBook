from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    return client['coockbookdb']



if __name__ == "__main__":   
  
    client = MongoClient()
    db=client.test
    storage = db.storage