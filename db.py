from pymongo import MongoClient

# A class to turn MongoDB language into simpler commands

def createDB(name):
    client = MongoClient()
    db = client.name


def add(object_name, to_db, to_collection):
    type = object_name.__class__.__name__

    if type == "List":
        # Lists do not have their own collection. Rather, they are included
        # as part of the document for their board. So, to "add" a board to
        # the db, we are actually updating the list's board document in
        # the board collection

        to_db.to_collection.update_one(
            {"name": object_name.board_name},
            {
                "$push": {"lists": object_name.getDocument()},
                "$currentDate": {"lastModified": True}
                }
        )
    else:
        result = to_db.to_collection.insert_one(object_name.getDocument())


    # TO DO
    # If adding a board, its ID should go into the document for the
    # project.

    #type = object_name.__class__.__name__
    #if type == "Board":
        # Should add the ObjectID of Board to its project's document
    #if type == "Card":
        # Should add the ObjectID of the Card to its lists

def delete(object_name, from_db, from_collection):
    from_db.from_collection.delete_one({"name": object_name.name})
