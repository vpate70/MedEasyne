from http.client import HTTPException
import transformers
import torch
import requests
import json
import os
from llama_cpp import Llama

# local parts taken from metal llama 3 hf website
# https://medium.com/@yingbiao/gpt-3-5-in-action-call-gpt-api-33157169794f

class LLM:
    def __init__(self, llm_type):
        if llm_type == "local":
            self.model_local = True
            self.model = Llama.from_pretrained(
                repo_id="SanctumAI/Meta-Llama-3-8B-Instruct-GGUF",
                filename="*Q4_1.gguf",
                n_gpu_layers=28, n_threads=6, n_ctx=3584, n_batch=521, verbose=True
        )
        else:
            self.model_type = False
            self.model = "gpt-3.5-turbo"
            self.url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Content-Type": "application/json"
            }
            self.api_key = os.getenv("API_KEY")
            
    def local_llm(self, user_desc, query):
        output = self.model.create_chat_completion(
                    messages = [
            {"role": "system", "content": f"You are extracting and defining difficult healthcare words from the input passage. Tailor the response to someone fitting the following description: \"{user_desc}\""},
            {"role": "user", "content": query},
        ],
            temperature=0.7,
            max_tokens=2000, 
            stop=["Q:"]
        )

        print(output)
        return output['choices'][0]['message']['content']
    

    def generate(self, message):
        if self.model_type:
            return self.local_llm(message)
        else:
            return self.send_request(message,0.6)

    def send_request(self, query, temperature):
        message_list = []
        system_message = {"role": "system", "content": "You are trying to define difficult healthcare words from the passage."}
        message_list.append(system_message)
        user_message = {"role": "user", "content": query}
        message_list.append(user_message)
    
        self.headers['Authorization'] = f"Bearer {self.api_key}"
        
        data = {
            "model": self.model,
            "temperature": temperature,
            "messages": message_list
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        response_json = response.json()
        
        if response.status_code == 200:
            content = [choice['message']['content'] for choice in response_json['choices']]
            return content[0]
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response_json}")
