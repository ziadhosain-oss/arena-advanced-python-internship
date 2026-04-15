import requests

# My webhook link
url = "https://webhook.site/5aad77a2-5a55-4177-9c2d-592ca094e12c"

# JSON body
data = {
    "name": "Ziad Hosain",
    "age": 22,
    "address": "Bangladesh",
    "phone_number": "+8801864838738"
}

# Send POST request with JSON
response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Server Response:", response.text)