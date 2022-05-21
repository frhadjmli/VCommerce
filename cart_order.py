import redis_connection, json, random, pprint

def product_to_cart():

    username = input("Enter Username:\n")
    profile = redis_connection.r.get(username)
    profile = json.loads(profile)
    print("\nAdd Products To Your Cart:\n")
    selected_products = []
    while(True):

        product_id = input(">>> Enter The product ID You Looking For...\n")
        selected_product = json.loads(redis_connection.r.get(product_id))
        selected_products.append(selected_product)
        input_option = input("""\n-- TO ADD MORE PRODUCTS PRESS '1'
-- TO STOP ADDING PRESS '2'\n""")
        if input_option == '2':
            for product in selected_products:
                profile['cart'].append(product)
            redis_connection.r.set(username, json.dumps(profile)) 
            break

    return profile

    
def submit_order(profile):

    order = {

        'order_products' : [],
        'order_payment' : 'N/A',
        'order_status' : 'N/A'
    }
    
    orders_ids = redis_connection.r.lrange("orders_ids", 0, -1) # Begin(Generates Order IDs )
    random_number = random.randint(100, 1000)
    random_id= "ORDER-" + str(random_number)
    if random_id not in orders_ids:
        order['order_id'] = random_id
        redis_connection.r.lpush("orders_ids", order['order_id'])
        
    else:
        order['order_id'] = f"ORDER-{random_number + 1}"
        redis_connection.r.lpush("orders_ids", order['order_id']) # End(Generates Order IDs )

    order['order_products'] = profile['cart'][:] #Copy Cart Products
    profile['cart'].clear()
    order['order_status'] = 'Reserved'
    profile['orders'].append(order)
    redis_connection.r.set(profile['username'], json.dumps(profile)) # updates user profile
    redis_connection.r.set(order['order_id'], json.dumps(order)) # updates order current status
    pprint.pprint(order)
    
    input_option = input("PAY AND CONCLUDE ORDER ?(y/n)")
    if input_option == 'y':

        total_price = 0
        for product in order['order_products']:
            item_no = int(input(f"\n>>> Enter Item Number For {product['product_name']}\n"))
            while(item_no > product['in_stock']):
                item_no = int(input(f"Select Less Equal Than {product['in_stock']}\n"))
            product['in_stock'] -= item_no
            redis_connection.r.set(product['product_id'], json.dumps(product)) # Updates Product in_stock Number Based on product_id
            redis_connection.r.set(product['product_id']+'_'+product['product_class'], str(product['in_stock'])) # Updates Product in_stock Number For Lists
            total_price += product['price'] * item_no

        order['order_status'] = 'Done'
        order['order_payment'] = total_price
        redis_connection.r.set(profile['username'], json.dumps(profile))
        redis_connection.r.set(order['order_id'], json.dumps(order)) # updates order current status
        print("\n   >>> Order Suceesfully Completes <<<\n")
        pprint.pprint(order) 

    else:

        order['order_status'] = 'Canceled'
        redis_connection.r.set(profile['username'], json.dumps(profile))
        redis_connection.r.set(order['order_id'], json.dumps(order))
        print("\n   >>> Order Canceled <<<\n")
        pprint.pprint(order)
        