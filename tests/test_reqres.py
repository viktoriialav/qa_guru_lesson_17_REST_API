import requests
import json

url = "https://reqres.in/api/users"

payload = {
  "name": "morpheus",
  "job": "leader"
}

response = requests.request("POST", url, data=payload)

print(response.text)
