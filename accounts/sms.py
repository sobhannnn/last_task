# import requests

def send_sms(phone_number, msg):
    url = "https://console.melipayamak.com/api/send/shared/8f892b16c22a4b3f89072fb00ee45cb6"
    bodyId = 57270
    args = [str(phone_number), str(msg)]


    body = { 
    "bodyId": bodyId, 
    "to": str(phone_number), 
    "args": args
    }
    # r = requests.post(url, json=body)\

    print(body)