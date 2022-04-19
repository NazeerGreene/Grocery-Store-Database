# Grocery Store Simulator
# Author: Na'zeer Greene
# CS360 Database Management

from ast import Break
from datetime import datetime as dt
from Grocery_Store_Manager import Inventory, Cart

import enum

DEBUG = False

class state(enum.Enum):
    AISLES = 1
    SHELF  = 2
    ADD_ITEM = 3
    CHECKOUT = 4
    LEAVE = 5

def print_aisle_layout(aisle_layout_dict):
    """Input: dictionary of (aisle number, aisle description) pairs.
    Output: Pretty board!
    Raises no errors."""

    # -------- banner set up --------
    banner_name = ' Aisles! '

    decorator_len = 30
    decorator_default = '*-'
    decorator = lambda x: decorator_default * x + decorator_default[0]

    per_side = int( (decorator_len - len(banner_name)) / 2)
    #---------------------------------

    print(decorator(per_side) + banner_name + decorator(per_side))

    for num, description in aisle_layout_dict.items():
        print('\t', str(num) + '. ', description)

    print( decorator(per_side*2 + int(len(banner_name)/ 2)) )



def print_inventory(list_of_Items, enum_offset=1):
    """Prints inventory for aisle, simulating a shelf.
    Raises no errors."""
    offset = 1

    for index, item in enumerate(list_of_Items, enum_offset):
        if item.get_count() > 0: # is item present?
            print(index, ' ',item)


def receipt(list_of_items):
    today = dt.now().strftime('%d %B %Y %I:%M %p')

    subtotal = 0
    tax_percent = 1.0928

    out = ''
    
    out += '\n'
    out += 'Greener Pastures Grocery Store'
    out += '\n'
    out += '\n'
    out += '\t9090 Lake Ontario Dr.'
    out += '\n'
    out += '\tSan Jose, CA 95134'
    out += '\n'
    out += '\t(408) 555 - 4545'
    out += '\n'
    out += '\n'
    out += f'Date: {today: >31}'
    out += '\n'
    out += f'Cashier: {"Nazeer" : >28}'
    out += '\n'
    out += '\n'
    out += f'{"QTY" : <10} {"Desc" : <20} {"Cost" : <5}'
    out += '\n'
    out += '-'*40
    out += '\n'

    for item in list_of_items:

        item_cost = round(item.get_count() * item.get_price(), 2)
        item_cost_str = str(item_cost).zfill(2)
        out += f'x{item.get_count(): <9} {item.get_name() : <20} {item_cost_str : <5}\n'

        subtotal += item_cost
        
    out += '-'*40 

    subtotal = round(subtotal, 2)
    total = round(subtotal*tax_percent, 2)
    tax = round((tax_percent - 1) * subtotal,2)

    subtotal_str = str(subtotal)
    tax_str = str(tax)
    total_str = str(total)

    out += '\n'
    out += f'Subtotal {subtotal_str : >20}'
    out += '\n'
    out += f'Tax {tax_str : >25}'
    out += '\n'
    out += f'Total {total_str : >23}'
    out += '\n'

    with open('Receipt.txt', 'w') as receipt:
        receipt.write(out)
    
    print(out)


def checkout(cart, inventory):
    pass


def add_item_to_cart(item, inventory):
    pass

# ------------- HELPER FUNCTIONS -------------
def get_int(prompt, min, max):

    user_int = None

    while None == user_int:
        user_input = input(prompt)

        if not user_input.isdigit():
            print('>>\tOnly integers!')
            print()
            continue

        user_int = int(user_input)
        if user_int > max or user_int < min:
            print(f'>>\tOnly integers between {min} and {max}.')
            print()
            user_int = None

    return user_int
    

def main():

    # we need an inventory manager to get the items for us
    inventory = Inventory('grocery_store_inventory.db')
    cart = Cart()

    aisles = inventory.get_aisles()
    # a cache so we don't have to call the database each time: key (aisle number); value (list of Item objects)
    aisles_inventory_cache = {}

    print()
    print('Welcome to Greener Pastures Grocery Store!')
    print('Enjoy the selection...')
    

    if DEBUG: print(aisles.keys())

    STATE = state.AISLES
    product_enumeration_offset = 1
    in_aisle = None

    while(True):

        if state.AISLES == STATE: #-------------------------------------------------------------

            print()
            print_aisle_layout(aisles)
            print()

            user_choice = get_int('Which aisle would you like to visit? >> ', 
            min(aisles.keys()), max(aisles.keys()))

            if DEBUG: print(f'user choice: {user_choice}')

            if user_choice not in aisles.keys():
                print('Let us visit an aisle listed above!')
                continue

            print(f'To the {aisles.get(user_choice)} aisle!')
            print()
            in_aisle = user_choice
            STATE = state.SHELF
        
        if state.SHELF == STATE: #-------------------------------------------------------------

            # check cache
            if user_choice not in aisles_inventory_cache.keys():
                # update cache
                aisles_inventory_cache[user_choice] = inventory.get_aisle_inventory(user_choice)

            STATE = state.ADD_ITEM

        if state.ADD_ITEM == STATE: #---------------------------------------------------------

            print()
            print_inventory(aisles_inventory_cache.get(in_aisle), product_enumeration_offset)

            user_choice = input('Choose a number to add item to cart or enter "back" >> ')
            user_choice = user_choice.lower()

            if 'back' == user_choice:
                STATE = state.AISLES
                continue
            
            # there's no point in continuing
            if not user_choice.isdigit():
                continue

            if DEBUG: print('[DEBUG] options: ', aisles_inventory_cache.get(in_aisle))
            user_int = int(user_choice)
            item_min = product_enumeration_offset
            item_max = item_min + len(aisles_inventory_cache.get(in_aisle)) - 1

            if  user_int < item_min or item_max < user_int:
                print(f'>>\tChoose an integer between {item_min} and {item_max} inclusive.')
                continue

            item_index = user_int - product_enumeration_offset
            item = aisles_inventory_cache.get(in_aisle)[item_index]

            # we have to check if the product is available in inventory
            print()
            if item.get_count() < inventory.product_quantity_for(item.get_ID()):
                print(f'\tAdding {item} to cart!')
                cart.add_item(item)
            else:
                print(f">>\tYou've already reached the max amount of {item.get_name()} in your cart.")
            print()

            #print(f'aisles dict: {aisles_inventory_cache.keys()}')

            #print(f'user_choice : {user_choice}')
            #print(f'inventory: {aisles_inventory_cache.get(user_choice)}')
            #print_inventory(aisles_inventory_cache.get(user_choice), product_enumeration_offset)

        if state.CHECKOUT == STATE: #-----------------------------------------------------------
            pass

        if state.LEAVE == STATE: #--------------------------------------------------------------
            print('Goodbye!')
            break
        
        

    '''
    shelf = inventory.get_aisle_inventory(1)

    print_inventory(shelf)

    for _ in range(3):
        cart.add_item(shelf[0])
        inventory.decrement_product_count_for(shelf[0].get_ID(), 1)
    
    cart.add_item(shelf[1])
    inventory.decrement_product_count_for(shelf[1].get_ID(), 1)


    print('In cart...')
    for item in cart.items():
        print(item.get_count(), '/', inventory.product_count_for(item.get_ID()) ,' ', item.get_name())
    
    #receipt(cart.items())

    print()
    print()
    '''

    


if __name__ == "__main__":
    main()
