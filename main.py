import discord
import apikeys as key
import MongodbHandler as MHD
import vertex_rest_api


intents = discord.Intents.default()
intents.messages = True
# User_Chat_History = {}

client = discord.Client(intents=intents)
user_database = MHD.MongodbHandler(key.MongoDB_uri,'Users','discord_users')
vertexAI = vertex_rest_api.VertexAPI(key.API_KEY,f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',key.PROJECT_ID)

User_data = {}
user_chat_history = []



# bot_prompt = "you are discord bot, you name is VertexAI bot, you help to provide user with answer the current user :"
f = open("prompt.txt",'r')
bot_prompt = f.read()


@client.event
async def on_ready():
    
    print(f'We have logged in as {client.user}')




@client.event
async def on_message(message):
    if client.user in message.mentions and message.author != client.user:
        if message.author == client.user:
            return

        if message.guild and message.content:
            if user_database.check_user(message.author.id) != True:
                user_database.create_one_User(message.author.display_name,message.author.id)
                user_database.create_one_section(message.author.id,message.author.display_name,'Bot')
            # insert user message with timestamp
            print(message.content)
            user_database.insert_user_message(message.content)
            
            
            # chatbison setup default for now
            vertexAI.set_parameters()
            context = bot_prompt + str(message.author.display_name)
            examples =[]
            chat_response = await vertexAI.chat_bison(context,examples,message.content,user_chat_history)
            
            
            
            # section = user_database.create_one_section(message.author.id,message.author.display_name,'ChatBot')
            
            # set a timestamp for bot message return and insert into section
            user_database.insert_bot_message(chat_response)
            user_database.insert_message(message.author.id)
            
            
            print(f"Palm2 reply to {message.author.display_name}: {chat_response}")
            # user_database.update_user_history(message.author.id,user_chat_history)
            await message.reply(chat_response)

client.run(key.DC_BOT_TOKEN)
