from collections import Counter
import math
import requests
import json
import time
full_response = []


data_bunch = [
    "Python is a language used for ai and machine learning",
    "Javascripta is a all rounder language can do both backend and frontend",
    "React-JS concference was held in bengaluru",
    "Go lang is the fastest language and can do multiple things",
    "Rust is evolving very rapidly because it is super fast",
    "Explore a new tech by reading tech news",
    "You can go to Geek for geeks for dsa classes",
    "Offline coding institutes like coding blocks and gfg are doing good job."
]


def cosine_similarity(query, document):
    query_tokens = query.lower().split(" ")
    document_tokens = document.lower().split(" ")
    query_counter = Counter(query_tokens)
    document_counter = Counter(document_tokens)
    dot_product = sum(query_counter[token] * document_counter[token] for token in query_counter.keys() & document_counter.keys())
    query_magnitude = math.sqrt(sum(query_counter[token] ** 2 for token in query_counter))
    document_magnitude = math.sqrt(sum(document_counter[token] ** 2 for token in document_counter))
    similarity = dot_product / (query_magnitude * document_magnitude) if query_magnitude * document_magnitude != 0 else 0
    return similarity

def return_response(query, corpus):
    similarities = []
    for doc in corpus:
        similarity = cosine_similarity(query, doc)
        similarities.append(similarity)
    return data_bunch[similarities.index(max(similarities))]


user_input = "my love is to build ai and machine laearning application"
start_time = time.time()

retrvant_document = return_response(user_input, data_bunch)
end_time = time.time()
print(f"retrvant_document: {retrvant_document}")
print(f"Execution time: {end_time - start_time} seconds")

#ollama llama 3

full_response = []
prompt = """
You are a bot that makes recommendations for activities. You answer in very short sentences and do not include extra information.
This is the recommended activity: {relevant_document}
The user input is: {user_input}
Compile a recommendation to the user based on the recommended activity and the user input.
"""

url = 'http://localhost:11434/api/generate'
data = {
    "model": "llama3",
    "prompt": prompt.format(user_input=user_input, relevant_document=retrvant_document)
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

try:
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            # print(decoded_line['response'])  # uncomment to results, token by token
            full_response.append(decoded_line['response'])
finally:
    response.close()
    
    
print(''.join(full_response))


