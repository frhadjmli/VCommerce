import base64, redis_connection, json


def costumer_register():

    with open("application/Pics/avatar.jpg", 'rb') as imagefile:
        profile_pic = base64.b64encode(imagefile.read()).decode('ascii')

    profile = {

        'username' : input("\nEnter username:\n"),
        'first_name':input("Enter First Name:\n"),
        'last_name':input("Enter Last Name:\n"),
        'password':input("Enter Password:\n"),
        'email':input("Enter Email:\n"),
        'phone':input("Enter Phone:\n"),
        'profile_pic':profile_pic,
        'cart':[],
        'orders':[]
        
    }

    redis_connection.r.set(profile['username'], json.dumps(profile))
    print("\n-----COSTUMER REGISTERED-----\n")






