import os

client_id = os.environ.get("AMAZON_LWA_CLIENT_ID")
client_secret = os.environ.get("AMAZON_LWA_CLIENT_SECRET")

print("Client ID:", client_id)
print("Client Secret:", client_secret)