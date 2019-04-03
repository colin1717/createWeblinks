#This script expects your Box App settings information saved in a file in this folder called config.json.  
#You can get this file from your App's configuraiton settings in the Box dev console. 


# Install SDK via pip
# $ pip install boxsdk

# Install JWT auth SDK
# $pip install boxsdk[jwt]

from boxsdk import JWTAuth
from boxsdk import Client
from boxsdk.exception import BoxAPIException
import json

#define Book mark information!!!!
weblink_url = "https://www.test.com"
weblink_title = "Request New Root Folder"
weblink_description = "Click this link to request a new root level folder"

#configure JWT auth object
sdk = JWTAuth.from_settings_file("./config.json")
client = Client(sdk)

#get enterprise users and their favorties' collection ID and assign them the users object
ent_users = client.users(user_type='all')

for user in ent_users:
    print('{0} (User ID: {1})'.format(user.name, user.id))

    #try to access user's collections and get user's collection ID, this will return the ID of the favorites collection 
    if client.as_user(client.user(user.id)).collections():
        try: 
            users_collections = client.as_user(client.user(user.id)).collections()
            for collection in users_collections:
                
                #add weblink to user 
                weblink_id = client.as_user(client.user(user.id)).folder(folder_id="0").create_web_link(weblink_url, weblink_title, weblink_description).id
                #add weblink to favorites
                client.as_user(client.user(user.id)).make_request(
                    'PUT',
                    'https://api.box.com/2.0/web_links/{0}'.format(weblink_id),
                    data = json.dumps({"collections": [{"id": collection.id}]})
                )


        except BoxAPIException as e:
            print(e.message)




    



