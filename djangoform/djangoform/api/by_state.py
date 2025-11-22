import sys

class State_dbQuery():
  """
  Class used for query/filter of the [national] db collection.
  """


  @classmethod
  def getAll(cls, dbCollection):
    """
    class method to retrieve all data

    columns returned: [ groupName, congregations, adherents]
    """
    listData = []
    try:
      if(dbCollection is not None):
        query = dbCollection.find({}, { "StateName": 1, "GroupName": 1, 'Congregations': 1, 'Adherents': 1, '_id':0 })

        #convert to dictionary object
        listData = list(query)


    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData


  @classmethod
  def querySearch(cls, dbCollection, searchQuery:str):
    """
    Class method to query the db using find params

    *must pass in two params: { dbCollection, searchQuery }

      Example:
        National_dbQuery.querySearch(dbCollection, searchQuery)
    """

    listData = []
    try:
      if(dbCollection is not None and searchQuery != ""):
        projection = {
          "StateName": 1,
          "GroupName": 1,
          'Congregations': 1,
          'Adherents': 1,
          'Adherents_percent_of_Total_Adherents': 1,
          'Adherents_percent_of_Population': 1,
          '_id':0
        }
        query = dbCollection.find({"GroupName": {"$regex": searchQuery, "$options": "i"}}, projection)
        listData = list(query)
        print(f"\n\n\n\n { listData } \n\n\n\n")

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData

