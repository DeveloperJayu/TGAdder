from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random

os.system("")
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
ye="\033[1;33m"
mg="\033[35m"
bl="\033[34m"

def banner():
    print(f"""  
{re} /__  ___/{gr} //   ) )  {cy}// | |                                      
{re}   / /    {gr}//        {cy}//__| |{ye}     ___   /  ___   /{mg}  ___{re}      __    
{re}  / /    {gr}//  ____ {cy} / ___  |{ye}   //   / / //   / /{mg} //___) ){re} //  ) ) 
{re} / /    {gr}//    / /{cy} //    | |{ye}  //   / / //   / /{mg} //       {re}//       
{re}/ /    {gr}((____/ /{cy} //     | |{ye} ((___/ / ((___/ /{mg} ((____   {re}//    
""")

banner()

print (re+"NOTE :")
print (gr+"1. Telegram only allow to add 200 members in group by one user.")
print (cy+"2. You can Use multiple Telegram accounts for add more members.")
print (ye+"3. Add only 50 members in group each time otherwise you will get flood error.")
print (mg+"4. Then wait for 15-30 miniute then add members again.")
print (bl+"5. Make sure you enable Add User Permission in your group")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print("[!] run python setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input('[+] Enter the code: '))

users = []
with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr+ '\n\n[+] Choose a group to add members:\n' +ye)
i = 0
j = 0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy + ' - ' + group.title)
    i += 1
g_index = input(gr+"\n[+] Enter a Number: "+cy)
target_group = groups[int(g_index)]
my_participants = client.get_participants(target_group)
my_participants_id = []
for my_participant in my_participants:
    my_participants_id.append(my_participant.id)

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input(gr+"Enter 1 to add by username or 2 to add by ID: "+cy))

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
        print(re+"Added too many users. Let me sleep for 60 seconds...")
        time.sleep(60)
    try:
        current = user['id']
        print(ye+"Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            print(ye+"Default mode selected...")
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        if user['id'] in my_participants_id:
            print(cy+"User already added.. so skipped")
            time.sleep(2)
            continue
        else:
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(ye+"Waiting for 10 Seconds...")
            time.sleep(10)
    except PeerFloodError:
        print(re+"Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print(ye+"Waiting {} seconds".format(100))
        time.sleep(100)
    except UserPrivacyRestrictedError:
        print(re+"The user's privaye settings do not allow you to do this. Skipping...")
        print(ye+"Waiting for 5 Seconds...")
        time.sleep(5)
    except UserBotError:
        print(re+"Can't add bot")
        time.sleep(5)
    except UserChannelsTooMuchError:
        print(re+"This user is already available in many groups/ channels. Skipping...")
        time.sleep(5)
    except UserNotMutualContactError:
        print(re+"This user is not mutual contact. Skipping...")
        time.sleep(5)
    except InputUserDeactivatedError:
        print(re+"This user is already deactivated. Skipping...")
        time.sleep(5)
    except:
        traceback.print_exc()
        print(re+"Unexpected Error")
        continue
