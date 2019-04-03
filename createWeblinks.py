# Install SDK via pip
# $ pip install boxsdk

# Install JWT auth SDK
# $pip install boxsdk[jwt]

from boxsdk import JWTAuth
from boxsdk import LoggingClient
from boxsdk.exception import BoxAPIException

#define service now form URL!!!!
servicenowform_url = "https://www.test.com"
servicenowform_title = "Request New Root Folder"
servicenowform_description = "Click this link to request a new root level folder"

#configure JWT auth object
sdk = JWTAuth.from_settings_file("./config.json")
client = LoggingClient(sdk)
service_account = client.user().get()
print('Service Account user name is {0}'.format(service_account.name))


#create dict for all user information, user id will be key, favorite collection ID will be value
users = {}


#get enterprise users and their favorties' collection ID and assign them the users object
ent_users = client.users(user_type='all')

for user in ent_users:
    print('{0} (User ID: {1})'.format(user.name, user.id))

    #get user collection ID and add to users object
    if client.as_user(client.user(user.id)).collections():
        try: 
            users_collections = client.as_user(client.user(user.id)).collections()
            for collection in users_collections:
                print(collection)
                users[user.id] = {"collection_id": collection.id}
                #add weblink to user and save ID in object
                weblink_id = client.as_user(client.user(user.id)).folder(folder_id="0").create_web_link(servicenowform_url, servicenowform_title, servicenowform_description).id
                users[user.id]["weblink_id"] = weblink_id


        except BoxAPIException as e:
            print(e.message)



print('users object')
print(users)

#For each user create new weblink


    



