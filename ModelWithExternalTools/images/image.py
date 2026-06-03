import base64
import ollama
import json

def image_task(prompt,**image_path):

    image_path = json.loads(image_path['image_path'])

    encoded_image_list = []
    for image in image_path:
        with open(image, "rb") as image_file:
            image_bytes = image_file.read()
            encoded_string = base64.b64encode(image_bytes).decode('utf-8')
            encoded_image_list.append(encoded_string)
    message = [{"role":"user","content":prompt,"images": encoded_image_list}]

    response = ollama.chat(
        model="qwen3.5:9b",
        messages=message
    )
    print(response['message']['content'])
    print("----------------------------------------------")
