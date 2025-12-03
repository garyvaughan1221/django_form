import sys

class County_dbQuery():
  """
  Class used for query/filter of the [national] db collection.
  """
  projection = {
    "StateName": 1,
    "CountyName": 1,
    "GroupName": 1,
    'Congregations': 1,
    'Adherents': 1,
    'Adherents_percent_of_Total_Adherents': 1,
    'Adherents_percent_of_Population': 1,
    '_id':0
  }

  # @classmethod
  # def getAll(cls, dbCollection):
  #   """
  #   class method to retrieve all data by Metro
  #   """
  #   listData = []
  #   try:
  #     if(dbCollection is not None):
  #       query = dbCollection.find({}, cls.projection)
  #       query = query.sort([("StateName", 1), ("CountyName", 1),("GroupName", 1)])

  #       #convert to dictionary object
  #       listData = list(query)

  #   except Exception as e:
  #       print("Error with MongoDB in by_county.getAll({cls}, {dbCollection}):", e, file=sys.stderr)
  #       sys.exit(2)

  #   finally:
  #     # print(f"{listData}")
  #     return listData



  @classmethod
  def getData(cls, dbCollection, searchQuery:str, selectedState:str, selectedCounty:str):
    """
    Class method to query the db using find params

    *must pass in 3 params: { dbCollection, searchQuery, selectedState }

    **optional param: {selectedCounty}

      Example:
        County_dbQuery.getData(dbCollection, searchQuery, subSearchQuery)

        --> with 4th param:
        County_dbQuery.getData(dbCollection, searchQuery, subSearchQuery, selectedCounty)
    """

    listData = []
    query = None
    try:
      if(dbCollection is None):
        raise Exception (f"No dbCollection for by_county.countySearch!: {dbCollection}")

      if(searchQuery == "all"):
        print(f"this is by_county.County_dbQuery.getData() =>", selectedState, searchQuery, selectedCounty)

        if(selectedCounty == "0"):
          print("county is 0")
          query = dbCollection.find(
            {"StateName": {"$regex": selectedState, "$options": 'i'}},
            cls.projection)
        else:
          print("county selected: ", selectedCounty)
          query = dbCollection.find(
            {"StateName": {"$regex": selectedState, "$options": 'i'},
            "CountyName": selectedCounty},
            cls.projection)

      else: # has a refined search query
        print("this is by_county.getData().-->\tSubSearchQuery", selectedState, selectedCounty, searchQuery)

        if(selectedCounty == "0"):
          query = dbCollection.find(
            {
              "StateName": {"$regex": selectedState, "$options": 'i'},
              "GroupName": {"$regex": searchQuery, "$options": "i"}
            },
            cls.projection)
        else:
          query = dbCollection.find(
            {
              "StateName": {"$regex": selectedState, "$options": 'i'},
              "CountyName": {"$regex": selectedCounty, "$options": 'i'},
              "GroupName": {"$regex": searchQuery, "$options": "i"}
            },
            cls.projection)

      if(query is not None):
        query = query.sort([("StateName", 1), ("CountyName", 1), ("GroupName", 1)])
        listData = list(query)
      # else:

    except Exception as e:
        print(f"Error with MongoDB queries in County_dbQuery.getData({cls}, {dbCollection}, {searchQuery}, {selectedState}, {selectedCounty})", e, file=sys.stderr)
        sys.exit(2)

    finally:
      # print("listData", listData)
      return listData

