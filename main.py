import discord
import loadenv as envkeys
import MongodbHandler as MHD
import VertexAPI as vertex_rest_api
import json
import aiohttp
import io
import PyPDF2
import re


intents = discord.Intents.default()
intents.messages = True
# User_Chat_History = {}

client = discord.Client(intents=intents)
user_database = MHD.MongodbHandler(envkeys.MongoDB_uri,'Users','discord_users')
vertexAI = vertex_rest_api.VertexAPI(envkeys.VERTEX_AI_API_KEY,f'https://us-central1-aiplatform.googleapis.com/v1/projects/{envkeys.VERTEX_AI_PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',envkeys.VERTEX_AI_PROJECT_ID)

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
    append_message = ""
    new_key = envkeys.VERTEX_AI_API_KEY
    if envkeys.get_gcloud_access_token() != None:
        new_key = envkeys.get_gcloud_access_token()

    vertexAI.set_header(new_key,f'https://us-central1-aiplatform.googleapis.com/v1/projects/{envkeys.VERTEX_AI_PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',envkeys.VERTEX_AI_PROJECT_ID)
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
                                text = text.replace('\n','')
                                append_message = "This is my pdf file : " + text  
        
            
        
        
        
        
        
        if message.guild and message.content and not new_section_command and message.author != client.user:
            
            if user_database.check_user(message.author.id) != True:
                user_database.create_one_User(message.author.display_name,message.author.id)
                user_database.create_one_section(message.author.id,message.author.display_name,'Bot')
                
                
                
            user_chat_history = user_database.find_latest_message(message.author.id)
             
            
            print(user_chat_history)
      
            # chatbison setup default for now
            vertexAI.set_parameters(0,0,0.95,40)
            context = "you are currently talking with user called : " + str(message.author.display_name) + bot_prompt 
            examples =pre_train_set['examples']
                
            
            
            pattern = r"<@\d+>"
            user_pure_input = re.sub(pattern,'',message.content)
            print(append_message)
            chat_response = await vertexAI.chat_bison(context,[],user_pure_input + append_message,user_chat_history)
            
            
            
            # section = user_database.create_one_section(message.author.id,message.author.display_name,'ChatBot')
            
            # set a timestamp for bot message return and insert into section
            user_database.insert_user_message(user_pure_input+append_message)
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

client.run(envkeys.DC_BOT_TOKEN)
