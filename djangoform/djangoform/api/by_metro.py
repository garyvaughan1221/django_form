import sys

class Metro_dbQuery():
  """
  Class used for query/filter of the [national] db collection.
  """
  projection = {
    "CBSACode": 1,
    "MetroName": 1,
    "GroupName": 1,
    'Congregations': 1,
    'Adherents': 1,
    'Adherents_percent_of_Total_Adherents': 1,
    'Adherents_percent_of_Population': 1,
    '_id':0
  }

  @classmethod
  def getAll(cls, dbCollection):
    """
    class method to retrieve all data by Metro
    """
    listData = []
    try:
      if(dbCollection is not None):
        query = dbCollection.find({}, cls.projection)
        query = query.sort([("MetroName", 1), ("GroupName", 1)])

        #convert to dictionary object
        listData = list(query)

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      # print(f"{listData}")
      return listData



  @classmethod
  def querySearch(cls, dbCollection, searchQuery:str):
    """
    Class method to query the db using find params

    *must pass in two params: { dbCollection, searchQuery }

      Example:
        Metro_dbQuery.querySearch(dbCollection, searchQuery)
    """

    listData = []
    try:
      if(dbCollection is not None and searchQuery != ""):
        query = dbCollection.find({"GroupName": {"$regex": searchQuery, "$options": "i"}}, cls.projection)
        query = query.sort([("MetroName", 1), ("GroupName", 1)])
        listData = list(query)

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData


  @classmethod
  def MetroSearch(cls, dbCollection, subSearchQuery:str, searchQuery:str=""):
    """
    Class method to query the db by metro area, for all church orgs in that state metro

    *must pass in two params: { dbCollection, searchQuery }

      Example:
        Metro_dbQuery.querySearch(dbCollection, searchQuery)
    """

    listData = []
    try:
      if(dbCollection is None):
        raise Exception ("No dbCollection for by_metro.metroSearch!")

      metroName = subSearchQuery
      if(metroName != "0" and searchQuery == "all"):
        print("this is by_metro.MetroSearch.searchQuery.ALL", metroName, searchQuery)
        query = dbCollection.find({"MetroName": metroName}, cls.projection)
        query = query.sort([("MetroName", 1), ("GroupName", 1)])
        listData = list(query)

      elif(subSearchQuery != "0" and (searchQuery != "all" and searchQuery != "")):
        print("this is by_metro.MetroSearch.searchQuery.-->\tSubSearchQuery", metroName, searchQuery, subSearchQuery)
        query = dbCollection.find(
          {
            "MetroName": {"$regex": metroName, "$options": 'i'},
            "GroupName": {"$regex": searchQuery, "$options": "i"}
          },
          cls.projection)

        query = query.sort([("MetroName", 1), ("GroupName", 1)])
        listData = list(query)

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData

