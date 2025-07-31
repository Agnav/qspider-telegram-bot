import requests
import json

session = requests.Session()

url = "https://golive.qspiders.com/api/student/web-login"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}
async def fetch(contact:str, password:str):

    payload =  {
        "contact": contact,
        "password": password
    }

    response = session.post(url, json=payload, headers=headers)
    status_code = response.status_code
    response_json = json.loads(response.text)
    user_id = response_json.get("id")
    user_name = response_json.get("name")

    return (user_name,user_id,status_code)






