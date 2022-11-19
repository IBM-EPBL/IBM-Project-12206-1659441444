import streamlit_authenticator as stauth

import database as db

"""usernames = ["pparker", "rmiller"]
names = ["Peter Parker", "Rebecca Miller"]
passwords = ["abc123", "def456"]
hashed_passwords = stauth.Hasher(passwords).generate()"""

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":passwords[1]
                }            
            }
        }
credentials = {
        "usernames":{
            "jsmith92":{
                "name":"john smith",
                "password":"$2b$12$TSuKwWML0EpbohBQgHx4p8E5q"
                },
            "tturner":{
                "name":"timmy turner",
                "password":"$2b$12$asdaUduuibuEIyBUBHASD896a"
                }            
            }
        }

credentials = {"usernames":{}}

for username, name, password in zip(usernames, names, passwords):
    user_dict = {"name":name,"password":password}
    credentials["usernames"].update({username:user_dict})


"""for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    db.insert_user(username, name, hash_password) """

