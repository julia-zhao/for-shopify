# using built-in db supplied by replit for ease-of-setup
# ideally would have liked to use a SQL database like MySQL
from replit import db
import replit
import json

main_message = """WELCOME TO INVENTORY
----------------------------------
Please choose:
create - to create an inventory
edit - to edit an inventory
delete - to delete an inventory
list - to list the inventory items
shipment - to create/edit a shipment
exit - to leave the app
----------------------------------
"""

def create_shipment(ship_name, inv_name, amount):
    # because the replit db does not account for dict types
    # we have to manually update all of this as a workaround to get nested db

    # check that the number to put into shipment is valid
    int_amount = int(amount)
    if int_amount < 0:
        print("amount to move into shipment is negative")
    else:
      # check if original inventory has enough to move into the shipment
      temp_val = db['inventory'][inv_name] 
      if temp_val < int_amount:
          print("not enough inventory to move!")
      else:
          db['inventory'][inv_name] = temp_val - int_amount
          # create shipment if it does not exist
          if ship_name not in db['shipment']:
              db['shipment'][ship_name] = {}
          # add/update inv into shipment
          temp_val = db['shipment'][ship_name]
          temp_val[inv_name] = int_amount 
          db['shipment'][ship_name] = temp_val
          print("success!")

def create_inventory(name, amount):
    # we do not want the user create an inventory that already exists
    if name in db['inventory']:
        print ("this inventory type already exists!")
    else:
        db['inventory'][name] = int(amount)
        print("inv create success!")

def edit_inventory(name, amount):
    # we do not want users to mistype and accidentally create a new inv type (e.g. a typo)
    if name not in db['inventory']:
        print("please create this inventory type first!")
    else:
        db['inventory'][name] = int(amount)
        print("inv edit success!")

def del_inventory(name):
    if name not in db['inventory']:
        print("this inventory type does not exist")
    else:
        del db['inventory'][name]
        print("inv delete success!")

def list_inventory():
    json_val = replit.database.dumps(db['inventory'])
    dict_val = json.loads(json_val)
    # print (dict_val.keys())
    print (dict_val)
  
def prompt_create_inv():
    name = input("Please enter inventory name:")
    amount = input("Please enter amount:")
    create_inventory(name, amount)

def prompt_edit_inv():
    name = input("Please enter inventory name:")
    amount = input("Please enter amount:")
    edit_inventory(name, amount)

def prompt_del_inv():
    name = input("Please enter inventory name:")
    del_inventory(name)

def prompt_ship():
    ship_name = input("Please enter shipment name:")
    inv_name = input("Please enter inventory name:")
    amount = input("Please enter amount:")
    create_shipment(ship_name, inv_name, amount)
  
if __name__ == '__main__':
    print(main_message)
    db['inventory'] = {'a':10}
    db['shipment'] = {}

    while(True):
        choice = input("Please make your choice: ").strip()
        if (choice == "create"):
            prompt_create_inv()
        elif (choice == "edit"):
            prompt_edit_inv()
        elif (choice == "delete"):
            prompt_del_inv()
        elif (choice == "list"):
            list_inventory()
        elif (choice == "shipment"):
            prompt_ship()
        elif (choice == "exit"):
            break