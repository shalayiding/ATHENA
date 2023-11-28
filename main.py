import discord
import apikeys as key
import vertexAPI as vai
import MongodbHandler as MHD

intents = discord.Intents.default()
intents.messages = True
# User_Chat_History = {}
client = discord.Client(intents=intents)
user_database = MHD.MongodbHandler(key.MongoDB_uri,'Users','discord_users')



@client.event
async def on_ready():
    
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if client.user in message.mentions and message.author != client.user:
        if message.author == client.user:
            return

        # if isinstance(message.channel, discord.channel.DMChannel):
        #     # message recive
        #     print(f'Received DM from {message.author}: {message.content}')
            
        #     # put in to the vertexai 
        #     chat_response = vai.chatbison(key.API_KEY,
        #                           f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',
        #                           key.PROJECT_ID,
        #                           message.content + "reply as much as you can.", chat_history," Your are discrod bot, name vertex AI")
        #     print(f"Palm2 reply to {message.author.display_name}: waiting for rest api")
        #     print(f"Palm2 reply: {chat_response['predictions'][0]['candidates'][0]['content']}")
            
        #     await message.channel.send(chat_response['predictions'][0]['candidates'][0]['content'])

        # reply to guild message using reply
        if message.guild:
            # print(f'Received DM from {message.author}: {message.content}')
            # put in to the vertexai 
            # if message.author.id not in User_Chat_History:
            #     User_Chat_History[message.author.id] = []
            if user_database.check_user(message.author.id) != True:
                user_database.Insert_one_User(message.author.display_name,message.author.id,[])
            user_chat_history = user_database.find_history(message.author.id)
            chat_response = vai.chatbison(key.API_KEY,
                                f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',
                                key.PROJECT_ID,
                                message.content+ " Space Holder ",  user_chat_history,"you are discord bot, you name is VertexAI bot, you help to provide user with answer the current user :" + message.author.display_name)
            
            # print(f"Palm2 reply to {message.author.display_name}: waiting for rest api")
            print(f"Palm2 reply to {message.author.display_name}: {chat_response['predictions'][0]['candidates'][0]['content']}")
            user_database.update_user_history(message.author.id,user_chat_history)
            await message.reply(chat_response['predictions'][0]['candidates'][0]['content'])

client.run(key.DC_BOT_TOKEN)
