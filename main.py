"""
curl -X 'POST' \
  'http://185.185.143.231:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'
curl -X 'PUT' \
  'http://185.185.143.231:5051/v1/account/1e7d94ce-7fc9-49ad-b64d-bac1eac0be82' \
  -H 'accept: text/plain'
"""


import requests
import pprint



# url = 'http://185.185.143.231:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
# json = {
#     "login": "alex_test",
#     "email": "alex_test@ya.ru",
#     "password": "12345678"
# }
#
# response = requests.post(url=url, headers=headers, json=json)
#
# print(response.status_code)
# pprint.pprint(response.json())



url = 'http://185.185.143.231:5051/v1/account/6e7d94de-7fc9-49ad-b64d-bac0eac0be82'
headers = {
    'accept': 'text/plain',
}


response = requests.put(url=url, headers=headers)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])