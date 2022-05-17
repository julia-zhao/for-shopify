# using built-in db supplied by replit for ease-of-setup
# ideally would have liked to use a SQL database like MySQL
from replit import db
import replit

def check_amount(amount, create=True):
    # either it is a digit or, we are editing and it is a digit with + or - in front
    if amount.isdigit():
        return {"msg": "success!", "pass": True, 'amount':int(amount), 'edit_type': 'none'}
    if not create and amount.startswith('-') and amount[1:].isdigit():
        return {"msg": "success!", "pass": True, 'amount':int(amount[1:]), 'edit_type': '-'}
    if not create and amount.startswith('+') and amount[1:].isdigit():
        return {"msg": "success!", "pass": True, 'amount':int(amount[1:]), 'edit_type': '+'}
    elif create: 
        return {"msg": "please input a positive integer for amount", "pass": False}
    else:
        return {"msg": "please input an integer amount with only +/- to modify it", "pass": False}
  
def valid_shipment(ship_name, inv_name, amount, create=True):
    # first check amount
    amount_valid = check_amount(amount, create)
  
    if amount_valid['pass']:
      new_amount = amount_valid['amount']
      edit_type = amount_valid['edit_type']
    else:
      return amount_valid['msg']

    # check if shipment already exists, create if it doesn't
    if create and ship_name in db['shipment']:
      return {"msg": "a shipment by this name already exists! please edit it", "pass": False}
    elif not create and ship_name not in db['shipment']:
      return {"msg": "there's no shipment by this name! please create it first", "pass": False}
      
    # check that inventory exists (we want to avoid typos)
    if inv_name not in db['inventory']:
        return {"msg": "make sure that inv name exists first!", "pass": False}
      
    inv_amount = db['inventory'][inv_name]
    if ship_name in db['shipment'] and inv_name in db['shipment'][ship_name]:
        ship_amount = db['shipment'][ship_name][inv_name]
    else:
        ship_amount = 0
  
    if edit_type == 'none':
        if new_amount < ship_amount:
            edit_type = '-'
            new_amount = ship_amount - new_amount
        else:
            edit_type = '+'
            new_amount = new_amount - ship_amount
          
    # check if original inventory has enough to move into the shipment
    if edit_type == '+' and new_amount > inv_amount:
        return {"msg": "not enough inventory to move!", "pass": False}
    # check if shipment has enough to move out to inventory
    if edit_type == '-' and new_amount > ship_amount:
        return {"msg": "not enough pieces in the shipment to take out!", "pass": False}

    return {"msg": "success!", "pass": True, 'new_amount': new_amount, 'edit_type': edit_type}

# create=True to create shipment, False to edit shipment
def create_edit_shipment(ship_name, inv_name, amount, create=True):
    shipment_valid = valid_shipment(ship_name, inv_name, amount, create)
    if shipment_valid['pass']:
      new_amount = shipment_valid['new_amount']
      edit_type = shipment_valid['edit_type']
    else:
      return shipment_valid['msg']

    # first edit the original inventory
    if amount.isdigit():
        new_amount = int(amount)
        edit_type = '+'
    else:
        new_amount = int(amount[1:])
        edit_type = amount[0]

    # create a shipment if it does not exist
    if create:
        db['shipment'][ship_name] = {inv_name: 0}
    elif inv_name not in db['shipment'][ship_name]:
        temp_val = db['shipment'][ship_name]
        temp_val[inv_name] = 0
        db['shipment'][ship_name] = temp_val
    # we take from inventory and put into shipment
    if (edit_type == '+'):
        db['shipment'][ship_name][inv_name] = db['shipment'][ship_name][inv_name] + new_amount
        db['inventory'][inv_name] = db['inventory'][inv_name] - new_amount
    # we take from shipment and put into inventory
    else:
        db['shipment'][ship_name][inv_name] = db['shipment'][ship_name][inv_name] - new_amount
        db['inventory'][inv_name] = db['inventory'][inv_name] + new_amount

    return "shipment create/edit success!"

def valid_inventory(name, amount, create=True):
    if create and name in db['inventory']:
        return {"msg": "this inventory already exists!", "pass": False}
    elif not create and name not in db['inventory']:
        return {"msg": "please create this inventory type first!", "pass": False}

    amount_valid = check_amount(amount, create)
  
    if amount_valid['pass']:
        new_amount = amount_valid['amount']
        if (create):
            return {"msg": "success!", "pass": True, 'new_amount': new_amount, 'edit_type': 'none'}
        else:
            edit_type = amount_valid['edit_type']
            inv_amount = db['inventory'][name]
            if (edit_type == '-' and new_amount > inv_amount):
                return {"msg": "trying to subtract more than we have!", "pass": False}
            return {"msg": "success!", "pass": True, 'new_amount': new_amount, 'edit_type': edit_type}
    else:
        return {'msg': amount_valid['msg'], 'pass': False}
  
def create_inventory(name, amount):
    inv_valid = valid_inventory(name, amount, True)
    if inv_valid['pass']:
        db['inventory'][name] = inv_valid['new_amount']
        return "inv creation success!"
    else:
      return inv_valid['msg']
          
def edit_inventory(name, amount):
    inv_valid = valid_inventory(name, amount, False)
    if inv_valid['pass']:
        new_amount = inv_valid['new_amount']
        inv_amount = db['inventory'][name]
        edit_type = inv_valid['edit_type']
        if (edit_type == 'none'):
            db['inventory'][name] = new_amount
        elif (edit_type == '+'):
            db['inventory'][name] = inv_amount + new_amount
        else:
            db['inventory'][name] = inv_amount - new_amount
        return "inv edit success!"
    else:
      return inv_valid['msg']
  
# note: this does not delete stuff that has already been assigned to shipments
def del_inventory(name):
    if name not in db['inventory']:
        return "this inventory type does not exist"
    else:
        del db['inventory'][name]
        return "inv delete success!" 
      
# note: this does not return the stuff inside the shipment back to inventory
def del_shipment(name):
    if name not in db['shipment']:
        return "this shipment does not exist"
    else:
        del db['shipment'][name]
        return "shipment delete success!" 
      
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
  