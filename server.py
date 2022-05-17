# using built-in db supplied by replit for ease-of-setup
# ideally would have liked to use a SQL database like MySQL
from replit import db

def create_shipment(ship_name, inv_name, amount):
    # because the replit db does not account for dict types
    # we have to manually update all of this as a workaround to get nested db

    # check that the number to put into shipment is valid
    if amount < 0:
        return "amount to move into shipment is negative"
    # check if original inventory has enough to move into the shipment
    temp_val = db['inventory'][inv_name] 
    if temp_val < amount:
        return "not enough inventory to move!"
    else:
        db['inventory'][inv_name] = temp_val - amount
    # create shipment if it does not exist
    if ship_name not in db['shipment']:
        db['shipment'][ship_name] = {}
    # add/update inv into shipment
    temp_val = db['shipment'][ship_name]
    temp_val[inv_name] = amount 
    db['shipment'][ship_name] = temp_val
    return "success!"

def create_inventory(name, amount):
    db[name] = amount

def edit_inventory(name, amount):
    db[name] = amount