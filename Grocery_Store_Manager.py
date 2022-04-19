import sqlite3 as sql

class Item:
    """A representation of a grocery store item."""
    
    def __init__(self, id, name, price, count):
        self.__ID = id
        self.__name = name
        self.__price = 0 if price < 0 else price
        self.__count = 0 if count < 0 else count
    
    def get_ID(self):
        return self.__ID
    
    def get_name(self):
        return self.__name
    
    def get_price(self):
        return self.__price

    def get_count(self):
        return self.__count
    
    def decrement_count(self):
        count =  self.__count - 1
        self.__count = 0 if count < 0 else count

    def increment_count(self):
        self.__count += 1

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.get_ID() == other.get_ID()
        return False
    
    def __str__(self):
        return '($' + str(self.__price) + ') ' + self.__name

    def __repr__(self):
        return 'Item( ' + ', '.join([str(self.__ID), str(self.__name), str(self.__price)]) + ', ' + str(self.__count) + ' )'


class Cart:
    """Class representation of a grocery store cart, holds Item objects."""

    def __init__(self):
        self.__cart = []

    def add_item(self, item):
        """Adds a single item to the cart if item is instance of Item class
        and if item has a count greater than zero.
        Raises no errors."""

        if not isinstance(item, Item):
            return 

        # if item is in list, then we just need to increment its count
        if item in self.__cart:
            idx = self.__cart.index(item)
            self.__cart[idx].increment_count()
        # otherwise add the new item
        else:
            self.__cart.append(item)

    def remove_item(self, item):
        """Removes a single item from the cart if item is instance of Item class.
        Raises no errors."""

        if isinstance(item, Item) and item in self.__cart:
            self.__cart.remove(item)

    def empty_cart(self):
        """Empties cart of items. Raises no errors."""

        self.__cart.clear()

    def items(self):
        """Returns a copy of a list of Item objects.
        Raises no error."""
        return self.__cart.copy()


class Inventory:
    """The interface between the grocery store database and client program."""

    def __init__(self, database_file):

        # there's no point in opening a file if it's not a database
        if not database_file.endswith('.db'):
            raise ValueError(f'Database files only: {database_file} does not end with .db')

        self.__db_file = database_file

        # open resource
        try:
            self.__conn = sql.connect(self.__db_file)
            # cursor allows us to write to database
            self.__cur = self.__conn.cursor()

        except sql.Error as err:
            raise ConnectionError('Operation Failed: ', err)
            self.__conn.close()
            exit()

        # we want to keep the aisle numbers and aisle products on hand
        self.__aisles_layout = self.__get_aisle_layout()
        # we want to keep the quantity per product on hand so that we 
        # don't give away more than we have
        self.__products_quantity = self.__get_quantities()
        #print('product quantity: ', self.__quantity)

    # ----------------- GETTERS -----------------

    def get_aisles(self):
        return self.__aisles_layout.copy()
    
    def get_aisle_inventory(self, aisle_num):
        """Returns the products in a specific aisle, refered to by aisle_num.
        Raises ConnectionError on failure to connect."""

        try:
            items_in_aisle_list = self.__cur.execute('''
            SELECT p.ID, p.name, p.price 
            FROM product p, AisleProductPlacement app 
            WHERE p.ID = app.product and app.aisle = ?;
            ''', (aisle_num,) ).fetchall()

            items = []

            for i in items_in_aisle_list:
                ID    = int(i[0])
                name  = i[1]
                price = round( float(i[2]), 2 )
                count = 1

                items.append( Item(ID, name, price, count) )

            return items

        except sql.Error as err:
            raise ConnectionError(f'Could not fetch aisle layout from database: {self.__db_file}')

        
    def product_quantity_for(self, product_ID):
        """Returns the count for product, identified by product ID; otherwise None.
        Raises no error."""

        return self.__products_quantity.get(product_ID)

    def decrement_product_quantity_for(self, product_ID, quantity):
        """Updates the count for a product, identified by product ID.
        Quantity should be a postive value: for example, if you have 3 items, then
        the proper call would be inventory.decrement_product_count_for(ID, 3).
        Returns None if quantity is less than 1; otherwise the new quantity integer for product
        Raises no error."""

        if (quantity < 1):
            return None

        if product_ID not in self.__products_quantity:
            return None

        count = self.__products_quantity.get(product_ID)
        count -= quantity
        count = 0 if count < 0 else count # minimum value for product's quantity
        self.__products_quantity[product_ID] = count
        return count
            
        

    
    # ----------------- HELPER FUNCTIONS -----------------
    def __get_aisle_layout(self):
        """Returns the aisles and their respective products from database.
        Raises ConnectionError on failure to connect."""

        try:
            aisles_list = self.__cur.execute('SELECT * FROM aisle;').fetchall()
            return { int(i[0]) : i[1] for i in aisles_list }

        except sql.Error as err:
            raise ConnectionError(f'Could not fetch aisle layout from database: {self.__db_file}')


    def __get_quantities(self):     
        """Returns the product ID and product count for each product in database.
        Raises ConnectionError on failure to connect."""

        try:
            product_list = self.__cur.execute('SELECT product, productCount FROM AisleProductPlacement;').fetchall()
            return { int(i[0]) : int(i[1]) for i in product_list }

        except sql.Error as err:
            raise ConnectionError(f'Could not fetch aisle layout from database: {self.__db_file}')


    def __del__(self):
        print('Deleting inventory and closing resources.')
        # release resources
        self.__conn.commit()
        self.__conn.close()
