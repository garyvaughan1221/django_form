import sys, json

class National_dbQuery():
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
        query = dbCollection.find({}, { "GroupName": 1, 'Congregations': 1, 'Adherents': 1, '_id':0 })

        #convert to dictionary object
        listData = list(query)


    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)

    finally:
      return listData

