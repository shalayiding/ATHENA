# Aierken
# REST API for Chatbot in Vertex AI

import requests
import base64
import json
import apikeys as key

api_key = key.API_KEY
endpoint_url = key.ENDPOINT_URL
project_id = key.PROJECT_ID






# given the api_key, endpoint url and project id to ask the vertex AI chatbot question and it return the json format
def chatbison(API_KEY,ENDPOINT_URL,PROJECT_ID,userinput, chathistory,context):
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'Content-Type': 'application/json; charset=utf-8'
    }
    chathistory.append({"author": "user","content" : userinput})
    
    payload = {
        "instances": [{
            "context":  context,
            
            "messages":chathistory,
        
        }],
        'parameters': {
            "temperature": 0.5,
            "maxOutputTokens": 2000
        }
    }
       
    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
    # print(response.json())
    if response.status_code == 200:
        data = response.json()
        chathistory.append({"author": "bot","content" :  data['predictions'][0]['candidates'][0]['content']})
    else:
        print(f"Error: {response.status_code}")
    return response.json()


# vertex ai image caption rest api call return json 
def imageCaption(API_KEY,ENDPOINT_URL,PROJECT_ID,image_url):
    response_image = requests.get(image_url)
    response_image.raise_for_status() 
    encoded_image = base64.b64encode(response_image.content).decode('utf-8')  
    payload = {
    'instances': [
        {
            'image': {
                'bytesBase64Encoded': encoded_image
            }
        }
    ],
    'parameters': {
        'sampleCount': 3,
        'language': 'en' 
        }
    }

    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)

    return response.json()
    
    
    
    
    
# vertex ai image visual Q&A api call return json
def ImageVisualQA(API_KEY,ENDPOINT_URL,PROJECT_ID,image_url,userinput):
    
    
    response_image = requests.get(image_url)
    response_image.raise_for_status() 
    encoded_image = base64.b64encode(response_image.content).decode('utf-8')  
    payload = {
    'instances': [
        {
            "prompt": userinput,
            'image': {
                'bytesBase64Encoded': encoded_image
            }
        }
        ],
        'parameters': {
            'sampleCount': 3,
            'language': 'en' 
        }
    }

    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)

    return response.json()
    




# using OCR to extraing text from the image 
def VertexAI_OCR(API_KEY,ENDPOINT_URL, PROJECT_ID, image_url):
    
    response_image = requests.get(image_url)
    response_image.raise_for_status()
    
    payload = {
        "requests": [
            {
                "image": {
                    "content": base64.b64encode(response_image.content).decode('utf-8')
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'x-goog-user-project': PROJECT_ID,
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)

    return response.json()




# print(VertexAI_OCR(key.API_KEY,
#                    f'https://vision.googleapis.com/v1/images:annotate',
#                    key.PROJECT_ID,
#                    image_url="https://gdoc.io/uploads/minimalist-menu-design-1-web-712x984.webp"))



# # image load 
# with open('dog_test.jpg', 'rb') as image_file:
#     encoded_image_data = base64.b64encode(image_file.read()).decode('UTF-8')

# print(imageCaption(key.API_KEY,
#                    f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/imagetext:predict',
#                    key.PROJECT_ID,
#                    image_url="https://designmodo.com/wp-content/uploads/2015/07/16-Taskade.jpg"))



# # image load 
# with open('dog_test.jpg', 'rb') as image_file:
#     encoded_image_data = base64.b64encode(image_file.read()).decode('UTF-8')

# print(ImageVisualQA(key.API_KEY,
#                    f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/imagetext:predict',
#                    key.PROJECT_ID,
#                    image_url="https://pbs.twimg.com/media/FUvqtImUsAA2I7B.png",
#                    userinput="descript this image ?"))



# chat_history = []
# test_image_url = "https://i.pinimg.com/originals/25/b4/6b/25b46b6de3faf76ff861df052a23c301.png"
# while True:
#     # response_image = requests.get("https://i.pinimg.com/originals/25/b4/6b/25b46b6de3faf76ff861df052a23c301.png")
#     # response_image.raise_for_status() 
#     # encoded_image = base64.b64encode(response_image.content).decode('utf-8')  
#     userinput = input("Your:")
#     chat_response = chatbison(key.API_KEY,
#                               f'https://us-central1-aiplatform.googleapis.com/v1/projects/{key.PROJECT_ID}/locations/us-central1/publishers/google/models/chat-bison:predict',
#                               key.PROJECT_ID,
#                               userinput, chat_history," Your are discrod bot, name vertex A")
#     print(chat_response)
#     print("Bot:" + chat_response['predictions'][0]['candidates'][0]['content'])


