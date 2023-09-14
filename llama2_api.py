import requests
from elasticsearch import Elasticsearch

search_results = {}

#Elastic configs & start 
ELASTIC_PASSWORD = "PPU90SH8Bt6kF3feQ3YpCqmM"

CLOUD_ID = "First_Deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ1ZDc5MWEyZTE3Mzc0MGQwOThmOTQ1Yjc2OWU5MzhkZCQ5NWI0NDY4YTAyM2Q0YmM0YmFlOWEzNDdhNjA1OGFkNA=="
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
#check elastic response 
client.info()

#AWS llama API
api_url = 'http://6323-34-91-48-125.ngrok-free.app/generate'

#ask user for question
question = input("Enter your question: ")



body = {
    "bool"  : {
        "must" : { 
            "match" : { "body_content" : question }
        },
        "filter" : {"bool": {"must": {"match_phrase": {"url_path_dir1": "en-au"}}}}
    }
}
result = client.search(index="search-microsoft", query=body)

print("Got %d Hits:" % result['hits']['total']['value'])
#for hit in result['hits']['hits']:
    # print(hit["_score"], hit["_source"]["title"])
    #search_results[hit["_source"]["title"]] = hit["_source"]["title"]
  #  print(search_results[hit["_source"]["title"]])
    #print(str(search_results))

search_results = result['hits']['hits'][0]["_source"]["url"]

llama_input = f"""
Answer the following question: {question} and also provide the following URL in your response: {search_results}
"""

#turn input into llama
llama_body = {
  "inputs": llama_input,  
 "parameters": {"max_tokens":256, "temperature":0.4}
}

r = requests.post(api_url, json=llama_body)

print(r.json())

