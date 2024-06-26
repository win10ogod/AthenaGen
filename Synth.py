import requests
import base64
import json
import os
import datetime
import glob

def generate_data(model, prompts, options=None, images=None, system=None, template=None, context=None, stream=False, raw=False, done=False, keep_alive="30m", output_json=False):
     url = "http://localhost:11434/api/generate"
    
     generated_texts = []
     json_data = []
    

     for prompt in prompts:
         payload = {
             "model": model,
             "prompt": prompt,
             "stream": stream,
             "top_p": 0.9,
             "temperature":0.7,
             "max_ctx":32768,
             "done":done,
             "raw": raw,
             "keep_alive": keep_alive
         }
        
         if images:
             encoded_images = [base64.b64encode(image).decode('utf-8') for image in images]
             payload["images"] = encoded_images
        
         if options:
             payload["options"] = options
        
         if system:
             payload["system"] = system
        
         if template:
             payload["template"] = template
        
         if context:
             payload["context"] = context
        
         response = requests.post(url, json=payload)
        
         print(f"API response status code: {response.status_code}")
         print(f"API response content: {response.text}")
        
         if response.status_code == 200:
             data = response.json()
             if isinstance(data, dict) and "response" in data:
                 generated_text = data["response"]
                 generated_texts.append(generated_text)
                 if output_json:
                     json_data.append({"instruction": prompt, "input": prompt, "output": generated_text})
             else:
                 print("API response format is incorrect")
         else:
             print(f"Request failed, status code: {response.status_code}")
    
     if output_json:
         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
         json_file_name = f"generated_texts_{timestamp}.json"
         with open(json_file_name, 'w', encoding='utf-8') as f:
             json.dump(json_data, f, indent=4, ensure_ascii=False)
         print(f"The generated JSON file has been saved to {json_file_name}")
    
     return generated_texts

def load_file(file_path):
     with open(file_path, 'r') as file:
         return file.read()

def load_prompts_from_file(file_path):
     with open(file_path, 'r') as file:
         prompts = file.readlines()
         prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
  
         return prompts


def save_to_file(file_path, texts):
     try:
         with open(file_path, 'w') as file:
             for text in texts:
                 file.write(f"{text}\n")
         print(f"The generated text has been saved to {file_path}")
     except IOError as e:
         print(f"Error saving file: {e}")

def create_output_file():
     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
     file_name = f"generated_texts_{timestamp}.txt"
     return file_name
    

def main():
     model = input("Please enter the model name: ")
     prompt_type = input("Please select the prompt type (1-input prompt, 2-load prompt from file:)")
     output_json = input("Whether to output a JSON file (yes/no): ")
     output_json = output_json.lower() == 'yes'
    
     if prompt_type == "1":
         prompts = []
         while True:
             prompt = input("Please enter the prompt (enter 'done' to complete): ")
             if prompt.lower() == 'done':
                 break
             prompts.append(prompt)
     elif prompt_type == "2":
         file_path = input("Please enter the file path: ")
         prompts = load_prompts_from_file(file_path)
  
     else:
         print("Invalid selection")
         return
    
     generated_texts = generate_data(model, prompts, output_json=output_json)
    
     if generated_texts:
         output_file = create_output_file()
         save_to_file(output_file, generated_texts)
     else:
         print("No text generated")

if __name__ == "__main__":
     main()
