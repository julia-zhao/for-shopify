# using built-in db supplied by replit for ease-of-setup
# ideally would have liked to use a SQL database like MySQL
from replit import db
import replit

# create=True to create shipment, False to edit shipment
def create_edit_shipment(ship_name, inv_name, amount, create=True):
    # check that the number to put into shipment is valid
    # check before casting to int
    if not amount.isdigit():
        return "please input a positive integer for amount"
    else:
        ship_amount = int(amount)
        if ship_amount < 0:
            return "amount of inventory to move into shipment must be at least 0"
        else:
        # check that inventory exists (we want to avoid typos)
        if inv_name not in db['inventory']:
            return "make sure that inv name exists first!"
        else:
            # check if original inventory has enough to move into the shipment
            orig_amount = db['inventory'][inv_name] 
            if orig_amount < ship_amount:
                return "not enough inventory to move!"
            else:
                db['inventory'][inv_name] = orig_amount - ship_amount
                if (create):
                    # make sure shipment does not exist, then create
                    if ship_name not in db['shipment']:
                        db['shipment'][ship_name] = {}
                    else:
                        return "a shipment by this name already exists! please edit it"
                else:
                    if ship_name not in db['shipment']:
                    return "there's no shipment by this name! please create it first"

                # add/update inv into shipment
                db['shipment'][ship_name][inv_name] = ship_amount 
                return "success!"

def create_inventory(name, amount):
    # we do not want the user create an inventory that already exists
    if name in db['inventory']:
        return "this inventory already exists!"
    else:
        # check before casting to int
        if amount.isdigit():
            db['inventory'][name] = int(amount)
            return "inv creation success!"
        else:
            return "please input a positive integer for amount"
          
def edit_inventory(name, amount):
    # we do not want users to mistype and accidentally create a new inv type (e.g. a typo)
    if name not in db['inventory']:
        return "please create this inventory type first!"
    else:
        # check before casting to int
        if amount.isdigit():
            db['inventory'][name] = int(amount)
            return "inv edit success!"
        else:
            return "please input a positive integer for amount"

# note: this does not delete stuff that has already been assigned to shipments
def del_inventory(name):
    if name not in db['inventory']:
        return "this inventory type does not exist"
    else:
        del db['inventory'][name]
        return "inv delete success!" 

def list_inventory():
    return replit.database.dumps(db['inventory'])

def list_shipments():
    return replit.database.dumps(db['shipment'])

# make sure that the db has the following keys
# there is no functionality in the app to clear the db, 
# so we don't need to make checks on if they exist later on
def init_db():
    if 'inventory' not in db.keys():
        db['inventory'] = {}
    if 'shipment' not in db.keys():
        db['shipment'] = {}
  