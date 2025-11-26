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

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData


  @classmethod
  def stateSearch(cls, dbCollection, subSearchQuery:str, searchQuery:str=""):
    """
    Class method to query the db by state for all church orgs in that state

    *must pass in two params: { dbCollection, searchQuery }

      Example:
        National_dbQuery.querySearch(dbCollection, searchQuery)
    """

    listData = []
    try:
      if(dbCollection is None):
        raise Exception ("No dbCollection for by_state.stateSearch!")

      projection = {
        "StateName": 1,
        "GroupName": 1,
        'Congregations': 1,
        'Adherents': 1,
        'Adherents_percent_of_Total_Adherents': 1,
        'Adherents_percent_of_Population': 1,
        '_id':0
      }
      selectedStateCode = int(subSearchQuery)
      # print("this is by_state.stateSearch.searchQuery", selectedStateCode, searchQuery)

      if(selectedStateCode != "0" and searchQuery == "all"):
        query = dbCollection.find({"StateCode": selectedStateCode}, projection)
        listData = list(query)

      elif(subSearchQuery != "0" and (searchQuery != "all" and searchQuery != "")):
        query = dbCollection.find({"StateCode": selectedStateCode, "GroupName": {"$regex": searchQuery, "$options": "i"}}, projection)
        listData = list(query)

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      # returnObj = getListOfStateNames(listData)
      # return returnObj
      return listData



# save this code for later...
# def getListOfStateNames(listData:list):
#     """
#     Helper function to group and get distinct state names
#       *I was too lazy to manually do it...lolz
#     """
#     df = pd.DataFrame(listData)
#     aggregated_df = df.groupby('StateCode')['StateName'].unique()
#     # print(aggregated_df)
#     returnObj = []
#     returnObj.append(listData)
#     returnObj.append(aggregated_df)
#     # print("\n\n statnames???")
#     # statenames = returnObj.get('stateNames')
#     print(aggregated_df)
#     return listData