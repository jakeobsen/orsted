#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import request
from datetime import datetime

# Login
# customer == email address
credentials = {
    "customer": "",
    "password": ""
}

# Login and get user data
headers = { 'x-customer-ip': "0.0.0.0", 'content-type': "application/json;charset=utf-8" }
response = request("POST", "https://api.obviux.dk/v2/authenticate", json=credentials, headers=headers)
data = response.json()

# Set user data
user_uuid = data['external_id']
token = data['token']
headers['authorization'] = token

# Get EAN number from deliveries (?)
response = request("GET", "https://api.obviux.dk/v2/deliveries", headers=headers)
data = response.json()

# Set ean number
ean = data[0]['ean']

# Get data
# For more fine grained control, change "daily" to:
# - hourly
# - daily
# - monthly
# - yearly
response = request("GET", f"https://capi.obviux.dk/v1/consumption/customer/{user_uuid}/ean/{ean}/daily", headers=headers)
data = response.json()

# Print rows
for c in data['data'][0]['consumptions']:
    start = datetime.strptime(c['start'], "%Y-%m-%dT%H:%M:%S.000Z")
    end = datetime.strptime(c['end'], "%Y-%m-%dT%H:%M:%S.000Z")
    kwh = c['kWh']
    print(f"{start.day}-{start.month}-{start.year}: {kwh} kWh")

