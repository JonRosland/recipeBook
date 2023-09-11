from pymongo import MongoClient


if __name__ == "__main__":   
  
    client = MongoClient("mongodb://localhost:27017")
    client.server_info()

    db = client["mydatabase"]
    print(db)

    print("5")
    mycol = db["customers"]

    print("4")
    mydict = { "name": "John", "address": "Highway 37" }
    print("6")
    x = mycol.insert_one(mydict)
    print("7")
    print(x.inserted_id)

    print("1")
    print(client.list_database_names())

    print("2")
    dblist = client.list_database_names()

    print("3")
    if "mydatabase" in dblist:
        print("The database exists.")