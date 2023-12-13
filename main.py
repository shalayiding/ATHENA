import discord
import apikeys as key
import MongodbHandler as MHD
import VertexAPI as vertex_rest_api
import json
import aiohttp
import io
import PyPDF2



intents = discord.Intents.default()
intents.messages = True
# User_Chat_History = {}

client = discord.Client(intents=intents)
user_database = MHD.MongodbHandler(key.MongoDB_uri,'Users','discord_users')
vertexAI = vertex_rest_api.VertexAPI(key.API_KEY,f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',key.PROJECT_ID)

User_data = {}

additional_message = {}


# bot_prompt = "you are discord bot, you name is VertexAI bot, you help to provide user with answer the current user :"
f = open("prompt.txt",'r')
bot_prompt = f.read()


pre_train_file = open("pre_train_set.txt",'r')
pre_train_set = json.load(pre_train_file)
print(pre_train_set)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')




@client.event
async def on_message(message):
    

    # if author is bot it self return 
    if message.author == client.user:
        return
    
    
    # event lister for the message mentions the bot
    if client.user in message.mentions:
        
        new_section_command = message.content.endswith('!section')
        if new_section_command and message.author != client.user:
            user_database.create_one_section(message.author.id,message.author.display_name,'Bot')
            user_database.insert_user_message(" ")
            user_database.insert_bot_message(" ")
            user_database.insert_message(message.author.id)
            await message.reply("New section is created history is clear.")
        
        
        
        # regx to extract the message.content pure 
        if message.attachments:
            for attachment in message.attachments:
                # Check if the attachment is a PDF file
                if attachment.filename.lower().endswith('.pdf'):
                    # Download the PDF file
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                data = io.BytesIO(await resp.read())
                                pdf_reader = PyPDF2.PdfReader(data)
                                page = len(pdf_reader.pages)
                                page_obj = pdf_reader.pages[0]
                                text = page_obj.extract_text()
                                additional_message[message.author.id] = "This is my pdf file : " + text  
                                print(additional_message.keys())
        
            
        
        
        
        
        
        if message.guild and message.content and not new_section_command and message.author != client.user:
            user_chat_history = user_database.find_latest_message(message.author.id)
            if user_database.check_user(message.author.id) != True:
                user_database.create_one_User(message.author.display_name,message.author.id)
                user_database.create_one_section(message.author.id,message.author.display_name,'Bot')
                  
            
            # print(user_chat_history)
      
            # chatbison setup default for now
            vertexAI.set_parameters(0,0,0.95,40)
            context = "you are currently talking with user called : " + str(message.author.display_name) + bot_prompt 
            examples =pre_train_set['examples']
            if message.author.id in additional_message:
                append_message = additional_message[message.author.id]
            else:
                append_message = ""
            
            chat_response = await vertexAI.chat_bison(context,examples,message.content + append_message,user_chat_history)
            
            # section = user_database.create_one_section(message.author.id,message.author.display_name,'ChatBot')
            
            # set a timestamp for bot message return and insert into section
            user_database.insert_user_message(message.content+append_message)
            user_database.insert_bot_message(chat_response)
            user_database.insert_message(message.author.id)
            
            # print(f"Palm2 reply to {message.author.display_name}: {chat_response}")
            # split process the bot response due to the discord api handel max char of 2000
            if len(chat_response) > 2000:
                chunks = [chat_response[i:i+2000] for i in range(0,len(chat_response),2000)]
                for chunk in chunks:
                    await message.reply(chunk)
            else:
                await message.reply(chat_response)

client.run(key.DC_BOT_TOKEN)
