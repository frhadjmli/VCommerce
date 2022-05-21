import redis_connection, json, pprint


def search_product():
    
    jsoned_products = []
    matched_products = []
    searched_item = input("\n>>> Search For...?\t")
    print(" >>> Results:\n")
    for word in searched_item.split():

        matched_products += redis_connection.r.lrange(word, 0, -1)

    matched_products = list(dict.fromkeys(matched_products)) # Removes Duplicates from List


    for product in matched_products:

        jsoned_product = json.loads(product)
        in_stock = redis_connection.r.get(jsoned_product['product_id']+'_'+jsoned_product['product_class']) # return most update value of in_stock
        jsoned_product['in_stock'] = int(in_stock)
        jsoned_products.append(jsoned_product)

    pprint.pprint(jsoned_products)       
    return jsoned_products

    