import requests

webhook_url = "https://webhook.site/5aad77a2-5a55-4177-9c2d-592ca094e12c"

data = {
    "name": "Ziad Hosain",
    "age": 22,
    "address": "Bangladesh",
    "phone_number": "+8801864838738"
}

response = requests.post(webhook_url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)