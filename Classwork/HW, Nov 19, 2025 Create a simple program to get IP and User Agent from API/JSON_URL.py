import requests

# Send GET request
response = requests.get("https://dummyjson.com/ip")

# Convert JSON response to Python dictionary
data = response.json()

# Print IP and User Agent
print("IP:", data["ip"])
print("User Agent:", data["userAgent"])