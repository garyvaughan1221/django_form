from djangoform.api.mongo_conn import get_client, get_db, close_client
import sys, atexit

# I could've just used a function instead of a class, but this is for example purposes
class DbClient():
    """
    Class to get MongoDB database from 2020USRC

    usage: myMongoDB = DBClient.getDB()
    """


    # reset dbConn to None before any actions
    def __init__(self):
        global theDB
        theDB = get_db()
        atexit.register(self.cleanup)

    def cleanup(self):
        # I'm guessing this is called at page_unload or something because I'm not seeing it execute after a dbRead call...
        print("closing DB connection")
        close_client()


    @classmethod
    def getDB(cls):
        """
        A class method to get the dbConnection open to query
        """

        try:
            client = get_client()
            # print("Connected to MongoDB server:", client.address)

            # If MONGODB_DB is set, show collections in that DB. Else list DB names.
            db_name = "2020USRC"
            if db_name: #could be a param...
                theDB = get_db()
                # print(f"Using DB: {db_name}")
                # print("Collections:", theDB.list_collection_names())

            return theDB

        except Exception as e:
            print("Error connecting to MongoDB:", e, file=sys.stderr)
            sys.exit(2)
