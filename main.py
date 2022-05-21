import redis_connection, profile_maker, product_maker
import product_search, product_showcase, cart_order



def main():

    print("-" * 120)
    print("\t\t\t\t\t>>> Welcome to VCOMMERCE <<<")
    print("-" * 120)
    print("\n>>> Please Choose One of The Following Actions:\n")
    print("""--Register Costumers: >>> Press 1

--Define a New Product: >>> Press 2

--List of Products: >>> Press 3

--Search for Products: >>> Press 4

--Add Products to The Cart: >>> Press 5

--To Quit App: >>> Press 0\n""")

    print('-'*40)

    selected_key = input("\n>>> Waiting For Your Input:\t")

    if selected_key == '1':
        profile_maker.costumer_register()
        main()
    elif selected_key == '2':
        product_maker.define_product()
        main()
    elif selected_key == '3':
        product_showcase.show_product()
        main()
    elif selected_key == '4':
        product_search.search_product()
        main()
    elif selected_key == '5':
        profile = cart_order.product_to_cart()
        input_option = input("\nProceed Purchase ?(y/n)\t\n")
        if input_option.lower() == 'y':
            cart_order.submit_order(profile)
        else:
            main()
        main()
    elif selected_key == '0':
        redis_connection.r.save()
        exit()
    else:
        print("\n>>> Invalid Input!")


if __name__ == '__main__':
    main()