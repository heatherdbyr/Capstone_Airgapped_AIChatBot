import requests

api_url = 'https://33myxc98ta.execute-api.ap-southeast-2.amazonaws.com/default/its-llama2'

json_body = {
 "inputs": [
  [
   {"role": "user", "content": "Can you search the internet?"}
  ]
 ],
 "parameters": {"max_new_tokens":256, "top_p":0.9, "temperature":0.6}
}

r = requests.post(api_url, json=json_body)

print(r.json())