import requests

# defining base url
BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/2", {"name": "None of ur business",
                                           "views": 999,
                                           "likes": 10})
print(response.json())

input()

response = requests.get(BASE + "video/1")
print(response.json())
input()

response = requests.get(BASE + "video/2")
print(response.json())
input()

response = requests.patch(BASE + "video/2", {"name": "Super new name", "likes": 101})
print(response.json())
input()

response = requests.patch(BASE + "video/2", {})
print(response.json())

