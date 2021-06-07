#==========================================================================================
# Part I: Installation and Configuration 
    # Step 1: Install telethon on your machine
    # Step 2: Authenticate your telegram account and get credentials
# N.B: Watch the video to know about how to install telethon and authenticate your account.
# Find the video link in the description/comment box
#==========================================================================================
# Part II: Writing Auto reply code
# Step 1: Import modules
import time, os, csv
from telethon import TelegramClient, events

# Step 2: Define your credentials
api_id = "3463304" # copy from my.telegram.org website
api_hash = '8ecafca60e2b5a867a15a3b0bbe7c347' # copy from the my.telegram.org website
phone = '+251973791994' # your phone number 
username = 'NuhaminEl'  # your username
#password = 'YOUR_PASSWORD'  #  use password if you have two-step verification enabled

# Message of the auto reply 
reply_msg = input("Enter your event:")

# Step 3: Instantiat the client object and establish the client connection
# use sequential_updates=True to respond to messages one at a time
client = TelegramClient(username, api_id, api_hash, sequential_updates=True).start(phone)

# Step 4: Define async main method
async def main():
    # Step 6: define the evnt handler method and handle the incoming message
    # This Python decorator will attach itself to the my_event_handler definition, 
    # and basically means that on a NewMessage event, the callback function 
    # you’re about to define will be called:
    @client.on(events.NewMessage(incoming=True))  # you can use incoming=True for messages that you receive
    # If for any reason you can’t use the @client.on syntax, don’t worry. 
    # You can call client.add_event_handler(callback, event) to achieve the same effect.
    async def my_event_handler(event):

        if event.is_private:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            if not from_.bot:  # don't auto-reply to bots

                print(time.asctime(), '-', event.message)  # optionally log time and message

                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                await event.reply(reply_msg) # you can use .resond()

                # Step 7: Save the log file into csv for further analysis
                msg = event.message.to_dict() # convert the log message to dict and save into a variable
                tl = time.asctime() # save the log date and time to the variable

                file_exists = os.path.isfile('log.csv') # find the path of the file and store in a variable
                with open('log.csv', 'a+') as log_file: # open the file and use a+ to overwrite the file
                    writer = csv.writer(log_file,delimiter=",",lineterminator="\n") # creating a writer
                    if not file_exists: # check the file is exist or not
                        # if the file is not exist then the writer write the headers
                        writer.writerow(['Message ID','user_id','Message','Date'])
                    else: 
                        # else the file is exist write row and append into the existing file                  
                        writer.writerow([event.id, from_.id, msg['message'], tl])

# the below code printing the start time
print(time.asctime(), '-', 'Auto-replying...')

# Step 5: Establish the client connection
with client:
    # the clien run untile completed
    client.loop.run_until_complete(main())
    # the client runs until the disconnected
    client.run_until_disconnected()
    # print(time.asctime(), '-', 'Stopped!')
    
