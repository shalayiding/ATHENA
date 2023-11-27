import discord
import apikeys as key
import vertexAPI as vai


intents = discord.Intents.default()
intents.messages = True
User_Chat_History = {}
client = discord.Client(intents=intents)



# loading start promtp
start_file = open("start.txt",'r')
start_text = start_file.read()


# loading tech questions 
tech_file= open("tech.txt",'r')
tech_text= tech_file.read()

# loading beh
beh_file = open("behavioural.txt")
beh_text = beh_file.read()




@client.event
async def on_ready():
    print(start_file)
    print(tech_file)
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
            if message.author.id not in User_Chat_History:
                User_Chat_History[message.author.id] = []
                
            chat_response = vai.chatbison(key.API_KEY,
                                f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',
                                key.PROJECT_ID,
                                message.content+ " Space Holder ",  User_Chat_History[message.author.id],"you are discord bot, you name is VertexAI bot, you help to provide user with answer the current user :" + message.author.display_name)
            # print(f"Palm2 reply to {message.author.display_name}: waiting for rest api")
            print(f"Palm2 reply to {message.author.display_name}: {chat_response['predictions'][0]['candidates'][0]['content']}")
            
            await message.reply(chat_response['predictions'][0]['candidates'][0]['content'])

client.run(key.DC_BOT_TOKEN)
