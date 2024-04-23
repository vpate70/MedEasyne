from http.client import HTTPException
import transformers
import torch
import requests
import json
import os

# local parts taken from metal llama 3 hf website
# https://medium.com/@yingbiao/gpt-3-5-in-action-call-gpt-api-33157169794f

class LLM:
    def __init__(self, llm_type):
        if llm_type == "local":
            self.model_local = True
            self.model_id = None
            self.pipeline = None
            self.terminators = None
        else:
            self.model_type = False
            self.model = "gpt-3.5-turbo"
            self.url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Content-Type": "application/json"
            }
            self.api_key = os.getenv("API_KEY")
            
    def local_llm(self, message):
        if self.model_id is None:
            self.model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

            self.pipeline = transformers.pipeline(
                "text-generation",
                model=self.model_id,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device_map="auto",
            )
            self.terminators = [
                self.pipeline.tokenizer.eos_token_id,
                self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]
        
        messages = [
            {"role": "system", "content": "You are defining difficult healthcare words from the passage."},
            {"role": "user", "content": message},
        ]

        prompt = self.pipeline.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
        )

        outputs = self.pipeline(
            prompt,
            max_new_tokens=256,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        return outputs[0]["generated_text"][len(prompt):]
    

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
