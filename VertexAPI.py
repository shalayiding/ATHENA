import aiohttp


class VertexAPI:
    def __init__(self,api_key,endpoint_url,project_id) -> None:
        """generate header for rest api

        Args:
            api_key (_type_): _description_
            endpoint_url (_type_): _description_
            project_id (_type_): _description_
        """
    
        self.set_header(api_key,endpoint_url,project_id)
    
    
    def set_header(self, API_KEY,ENDPOINT_URL,PROJECT_ID):
        self.API_KEY = API_KEY
        self.ENDPOINT_URL = ENDPOINT_URL
        self.PROJECT_ID = PROJECT_ID
        self.HEADER = {
        'Authorization': 'Bearer {}'.format(self.API_KEY),
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    
    def set_parameters(self,temperature=0,maxOutputTokens=0,topP=0.95,topK=40):
        """set parameters value for the rest api if nothing comes in go with default value 

        Args:
            temperature (int, optional): _description_. Defaults to 0.
            maxOutputTokens (int, optional): _description_. Defaults to 0.
            topP (float, optional): _description_. Defaults to 0.95.
            topK (int, optional): _description_. Defaults to 40.
        """
        self.PARAMETERS = {'parameters': 
            {
            "temperature": temperature,
            "maxOutputTokens": maxOutputTokens,
            "topP": topP,
            "topK": topK
            }} 


    def set_instance(self,context,examples,messages):
        """instance of the payload

        Args:
            context (_type_): _description_
            examples (_type_): _description_
            messages (_type_): _description_
        """
        self.INSTANCE = {"instances":
            [{
            "context":  context,
            "examples":examples,
            "messages":messages,
            }]
            } 
        
        
    async def chat_bison(self,context,exmaples,userinput,messages):
        """this is main function that will call rest api 

        Args:
            context (_type_): _description_
            exmaples (_type_): _description_
            userinput (_type_): _description_
            messages (_type_): _description_

        Returns:
            string: vertexAI response
        """
        messages.append({"author": "user","content" : userinput})
        self.set_instance(context,exmaples,messages)
        payload = {
            **self.INSTANCE,
            **self.PARAMETERS
        }
        try :
            async with aiohttp.ClientSession() as session:
                async with session.post(self.ENDPOINT_URL, headers=self.HEADER, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        messages.append({"author": "bot","content" :  data['predictions'][0]['candidates'][0]['content']})
                        return data['predictions'][0]['candidates'][0]['content']    
                    else:
                        return "Error with REST API call:" + str(response.status)
        except Exception as e :
            return "The has been error with REST API call: "+ str(e) + "statues code of the api is :"+ str(response.status)
        
        
        
