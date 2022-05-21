# lists all the products based on their class(category)
# and sorts them by price
import redis_connection, json, pprint


def show_product():
    
    asked_class = input("Enter Desired Product Class:(Smartphone,Laptop,Clothes)\n")
    products = redis_connection.r.lrange(asked_class, 0, -1)
    jsoned_products = []
    for product in products:
        
        jsoned_product = json.loads(product)
        in_stock = redis_connection.r.get(jsoned_product["product_id"]+'_'+jsoned_product['product_class']) # return most update value of in_stock
        jsoned_product['in_stock'] = int(in_stock)
        jsoned_products.append(jsoned_product) # convert string to json/dict

    pprint.pprint(jsoned_products)

    while(True):

        price_order = input("\n>>> Select Price Order(Ascending = 1 , Descending = 2):\n")
        
        if price_order == '1':
            ordered_products = sorted(jsoned_products, key=lambda dict: dict['price'])
            pprint.pprint(ordered_products)
            break
        elif price_order == '2':
            ordered_products = sorted(jsoned_products, key=lambda dict: dict['price'], reverse=True)
            pprint.pprint(ordered_products)
            break
        else:
            print(">>> Invalid Input, Try again")
            show_product()