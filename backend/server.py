from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongo://localhost:27017"
    host = "localhost"
    port = "27017"
    user = "root"
    password = "example"
    db_name = "mongo"
    auth_mechanism = "SCRAM-SHA-1"
    uri = "mongodb://"+user+":"+password+"@"+host+":"+port+"/"+db_name+"?"+"authMechanism="+auth_mechanism
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(uri)

    except ConnectionFailure:
        print("Server not available")
        return None
   
    # Get reference to your database
    return client['coockbookdb']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
    db = get_database()

    if db:
        # Perform some basic operations to check the connection
        collection = db['coockbook']
        
        # Insert a test document
        res = collection.insert_one({"test": "test_value"})
        print("Document inserted with id", res.inserted_id)
        
        # Fetch all documents
        for doc in collection.find():
            print(doc)
    #client.server_info()

    #except pymongo.errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    #print(err)
 
   # Create the database for our example (we will use the same database throughout the tutorial
    #return client['coockbookdb']
  
# This is added so that many files can reuse the function get_database()
#if __name__ == "__main__":   
  
   # Get the database
   # db = get_database()
    #db.createCollection('coockbook')
