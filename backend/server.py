# using built-in db supplied by replit for ease-of-setup
# ideally would have liked to use a SQL database like MySQL
from replit import db
import replit
import json

# create=True to create shipment, False to edit shipment
def create_edit_shipment(ship_name, inv_name, amount, create=True):
    # check that the number to put into shipment is valid
    int_amount = int(amount)
    if int_amount < 0:
        return "amount of inventory to move into shipment must be at least 0"
    else:
      # check that inventory exists (we want to avoid typos)
      if inv_name not in db['inventory']:
        return "make sure that inv name exists first!"
      else:
        # check if original inventory has enough to move into the shipment
        temp_val = db['inventory'][inv_name] 
        if temp_val < int_amount:
            return "not enough inventory to move!"
        else:
            db['inventory'][inv_name] = temp_val - int_amount
            if (create):
              # make sure shipment does not exist, then create
              if ship_name not in db['shipment']:
                db['shipment'][ship_name] = {}
              else:
                return "a shipment by this name already exists!"
            else:
                if ship_name not in db['shipment']:
                  return "there's no shipment by this name!"

            # add/update inv into shipment
            temp_val = db['shipment'][ship_name]
            temp_val[inv_name] = int_amount 
            db['shipment'][ship_name] = temp_val
            return "success!"

def create_inventory(name, amount):
    # we do not want the user create an inventory that already exists
    if name in db['inventory']:
        return "this inventory already exists!"
    else:
        db['inventory'][name] = int(amount)
        return "inv creation success!"

def edit_inventory(name, amount):
    # we do not want users to mistype and accidentally create a new inv type (e.g. a typo)
    if name not in db['inventory']:
        return "please create this inventory type first!"
    else:
        db['inventory'][name] = int(amount)
        return "inv edit success!"

def del_inventory(name):
    if name not in db['inventory']:
        return "this inventory type does not exist"
    else:
        del db['inventory'][name]
        return "inv delete success!"

def list_inventory():
    json_val = replit.database.dumps(db['inventory'])
    dict_val = json.loads(json_val)
    return dict_val

def list_shipments():
    json_val = replit.database.dumps(db['shipment'])
    dict_val = json.loads(json_val)
    return dict_val
  
def init_db():
    if 'inventory' not in db.keys():
        db['inventory'] = {}
    if 'shipment' not in db.keys():
        db['shipment'] = {}
  