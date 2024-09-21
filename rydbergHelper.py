import sys,os
import requests
import pandas as pd

client_ID = "02e805b7-77ee-11ef-b441-6d6e84e75559"
API_key = "eyJraWQiOiIwIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJpWmV0dGxlIiwiYXVkIjoiQVBJIiwiZXhwIjoyNjczNjEyNzM2LCJzdWIiOiJlNGJiZDM5MC1jYmEwLTExZTctYTlhYS1jOWQ4ZmYzZDk3MWQiLCJpYXQiOjE3MjY5MDQ5NjAsImNsaWVudF9pZCI6IjAyZTgwNWI3LTc3ZWUtMTFlZi1iNDQxLTZkNmU4NGU3NTU1OSIsInR5cGUiOiJ1c2VyLWFzc2VydGlvbiIsInVzZXIiOnsidXNlclR5cGUiOiJVU0VSIiwidXVpZCI6ImU0YmJkMzkwLWNiYTAtMTFlNy1hOWFhLWM5ZDhmZjNkOTcxZCIsIm9yZ1V1aWQiOiJlNGJhNzQwMC1jYmEwLTExZTctOGJmYi1lMjA3NzRhZWEwZjUiLCJ1c2VyUm9sZSI6Ik9XTkVSIn0sInNjb3BlIjpbIlJFQUQ6UFJPRFVDVCJdfQ.ITx5w9cuNr7CeCrR4mZGD5XTITWy201VQoiiTUQ_q5rR9wDkBTnoP1mWqP76TGgbgwrRsvFXAyyues2FMhbhAuuZF3pFJoKOt5fwWB2b1xJ8Z2iPSOq33WnONDiwNtvLCwK152FxhDYWL4SFo2bjtG_bOyMrN4d4g5dJlyazR9WSohk1kYGkgVavpe96RaIzW3LPM4MQhFfz7oHqAfUkOiMKYx6GB7jQikaFIvgZHm4G3NmY_AsBGLM48ZNz2PoJa6j9mSYOgwrqKfUvOHpyRqHHIS1uoSEFfCq6KdKAVcpYfFh7qKMkXkobFtd7Wnfaa5BMHgx17dA8mG4nTtKiTg"

# Define the URL
post_url = "https://oauth.zettle.com/token"

# Define the headers
post_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Define the data payload
post_data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "client_id": f"{client_ID}",
    "assertion": f"{API_key}"     
}

access_request = requests.post(post_url, headers=post_headers, data=post_data)

access_data = access_request.json()
bearer_token = access_data.get("access_token")


library_url = "https://products.izettle.com/organizations/self/library"
stock_url = "https://inventory.izettle.com/v3/stock"
get_headers = {
    "Authorization": f"Bearer {bearer_token}",  
}

library_response = requests.get(library_url, headers=get_headers)
stock_response = requests.get(stock_url, headers=get_headers)

products_data = library_response.json().get("products")
stock_data = stock_response.json()

class Product:
    def __init__(self, uuid, name, category, price, balance):
        self.uuid = uuid
        self.name = name
        self.category = category
        self.price = price
        self.balance = balance
    
    def print(self):
        print(f"UUID: {self.uuid}")
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Price: {self.price}")
        print(f"Balance: {self.balance}")

list_products = []


for i in products_data:
    list_products.append(Product(
        i.get("uuid"),
        i.get("name"),
        i.get("category").get("name"),
        i.get('variants')[0].get("price").get("amount")/100,
        0
        )
    )

for i in stock_data:
    uuid = i.get("productUuid")
    balance = i.get("balance")
    for j in list_products:
        if j.uuid == uuid:
            j.balance = balance
        if j.category not in["Wine", "Beer", "Cider"]:
            j.balance = "--"


for i in list_products:
    print("--------------------------")
    i.print()
