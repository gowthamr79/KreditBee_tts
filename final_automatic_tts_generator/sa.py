import time

import requests
import json

url = "http://20.81.186.199/tts_generate/wav"

payload = json.dumps({
  "message": "As per your promise, please make the payment before 07 June 2021. May you've a great day!",
  "template_name": "utter_first_case_inform_payment_date"
})
headers = {
  'Content-Type': 'application/json'
}
count = 0
session = requests.session()
while True:
    start_time = time.time()
    response = session.request("POST", url, headers=headers, data=payload)
    print(time.time() - start_time)
    time.sleep(3)
    # print(response.text)
    count += 1
    if count >5:
        break