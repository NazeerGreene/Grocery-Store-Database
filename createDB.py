from random import uniform

def productTuple(products, productIDStart=0, priceLower=0, priceUpper=10000000):
    
    fullProducts = []

    productID = productIDStart

    for product in products:
        price = round(uniform(priceLower, priceUpper), 2)
        
        fullProduct = [productID, product, price]

        fullProducts.append(fullProduct)

        productID += 1

    return fullProducts


dairy = [ 'milk', 'cheese', 'yogurt', 'cream cheese' ]
fruit = [ 'bag of apples', 'cherries', 'bag of peaches', 'grapes' ]
clothes = [ 'shirt', 'pants', 'shoes', 'bathroom robe']
hygiene = [ 'toothpaste', 'shower gel', 'shampoo', 'conditioner' ]

aisles = { 'dairy': [], 'fruit': [], 'clothes': [], 'hygiene': [] }
aisles_desc = { 
    'dairy': 'Dairy Products!', 
    'fruit': 'Fruits!', 
    'clothes': 'Shirts, Shoes, and More!', 
    'hygiene': 'Showers Gels and Fresh Smells!' }

productStart = 0
aisles['dairy'] = productTuple(dairy, productIDStart=productStart, priceLower=2.50, priceUpper=4.99)

productStart += len(dairy)
aisles['fruit'] = productTuple(fruit, productIDStart=productStart, priceLower=3.45, priceUpper=7.50)

productStart += len(fruit)
aisles['clothes'] = productTuple(clothes, productIDStart=productStart, priceLower=16.50, priceUpper=34.65)

productStart += len(clothes)
aisles['hygiene'] = productTuple(hygiene, productIDStart=productStart, priceLower=7.99, priceUpper=19.99)

aisleStart = 1

aislenum = aisleStart
for aisle, item_list in aisles.items():
    for i in item_list:
        print(f'INSERT INTO Product VALUES {i[0], i[1], i[2]};')
    for i in item_list:
        print(f'INSERT INTO AisleProductPlacement VALUES {i[0], aislenum, 20};')
    aislenum += 1

for num, desc in enumerate(aisles_desc.values(), aisleStart):
    print(f'INSERT INTO Aisle   VALUES {num, desc};')



with open('grocery_store.txt', 'w') as db:
    db.write("""
CREATE TABLE IF NOT EXISTS Product 
(
    ID int primary key,
    name varchar(30),
    price numeric(6, 2)
);
CREATE TABLE IF NOT EXISTS AisleProductPlacement 
(
    product int,
    aisle int,
    quantity int
);
CREATE TABLE IF NOT EXISTS Aisle 
(
    aisleNumber int primary key,
    description varchar(30)
);
""")

    db.write('\n')

    aislenum = aisleStart
    for aisle, item_list in aisles.items():
        for i in item_list:
            db.write(f'INSERT INTO Product VALUES {i[0], i[1], i[2]};\n')
        for i in item_list:
            db.write(f'INSERT INTO AisleProductPlacement VALUES {i[0], aislenum, 20};\n')
        aislenum += 1
    
    for num, desc in enumerate(aisles_desc.values(), aisleStart):
        db.write(f'INSERT INTO Aisle   VALUES {num, desc};\n')
