# submits a new product
import redis_connection, json, random


def define_product():
    
    product = {
        
        'product_class' : input("\nEnter Product Class:(Smartphone,Laptop,Clothes,...)\n"),
        'product_name' : input("Enter Product Name:\n"),
        'in_stock' : int(input("Enter Stock Number:\n")),
        'price' : int(input("Enter Price:\n")),
        'product_detail' : input("Enter Product Specs:\n")

    }

    in_stock = product['in_stock']

    product_ids = redis_connection.r.lrange("product_ids", 0, -1) # Begin(Generates Product IDs )
    random_number = random.randint(10000, 100000)
    random_id = "KALA-" + str(random_number)
    if random_id not in product_ids:
        product["product_id"] = random_id
        redis_connection.r.lpush("product_ids", product["product_id"])

    else:
        product["product_id"] = f"KALA-{random_number + 1}"
        redis_connection.r.lpush("product_ids", product["product_id"]) # End(Generates Product IDs )


    for word in product["product_name"].split(): # Indexing Product Names For Search Part
        redis_connection.r.lpush(word, json.dumps(product))

    for word in product["product_detail"].split(): # Indexing Product Details For Search Part
        redis_connection.r.lpush(word, json.dumps(product))


    redis_connection.r.set(product["product_id"], json.dumps(product)) # convert dict to string
    redis_connection.r.lpush(product["product_class"], json.dumps(product))
    redis_connection.r.set(product["product_id"]+'_'+product['product_class'], str(in_stock))
    print("\n-----PRODUCT REGISTERED-----\n")