import datetime
import hashlib
import json
import os
import re

from pydub import AudioSegment

import hindi_date_processor
import hindi_number_processor

with open("../bot_responses.json", "r+") as f:
    data = json.load(f)

with open("../customer_details_hindi.json", "r+") as f:
    customer_details = json.load(f)
# print(customer_details)

general_entities_responses = []
ptp_entities_responses = []

general_entities = ["monthly_emi","emi_amount","amount","partial_payment_amount","ptp_partial_amount","total_emi","no_of_loans"]
ptp_entities = ["ptp_day","emi_date","ptp_date","monthly_emi_date"]
for item in data:
    # if 'Hindi Responses' in item:
    text = item["Hindi"]
    matches = re.findall(r"\{(.*?)\}", text)
    if matches:
        for match in matches:
            if match in general_entities:
                if text not in general_entities_responses:
                    general_entities_responses.append(text)
            if match in ptp_entities:
                if text not in ptp_entities_responses:
                    ptp_entities_responses.append(text)


# print(general_entities_responses)
# print(ptp_entities_responses)


# def get_formatted_response(response):
#     matches = re.findall(r"\{(.*?)\}", response)
#     matches = ["{" + item + "}" for item in matches]
#     split_regex = ""
#     for item in range(len(matches)):
#         if item != len(matches) - 1:
#             split_regex += matches[item] + " | "
#         else:
#             split_regex += matches[item]
#     sub_strings = re.split(split_regex, response, flags=1)
#     sub_strings.extend(matches)
#     positions = {}
#     formatted_responses = []
#     for sub_string in sub_strings:
#         if sub_string == ".":
#             continue
#         positon = response.find(sub_string)
#         positions[positon] = sub_string
#     for item in sorted(positions):
#         formatted_responses.append(positions[item])
#     # print(formatted_responses)
#     return formatted_responses

def get_formatted_response(response):
    print("Response:",response)
    matches = re.findall(r"\{(.*?)\}", response)
    matches = ["{" + item + "}" for item in matches]
    print("Matches:",matches)
    splitted=[]
    for rule in matches:
        pos=response.find(rule)
        splitted.append(response[:pos])
        splitted.append(rule)
        response=response[pos+len(rule):]
    if len(response)>0:
        splitted.append(response)
    print(splitted)
    return splitted


final_entity_responses = []


for customer in customer_details:
    for response in general_entities_responses:
        matches = re.findall(r"\{(.*?)\}", response)
        matches = ["{" + item + "}" for item in matches]
        formatted_response = get_formatted_response(response)
        final_voice = None
        entities = {}
        for item in formatted_response:
            if item in matches:
                if item == "{monthly_emi}":
                    entities["monthly_emi"] = customer["emi_amt"]
                    # print("********",customer["phone_number"])
                    number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                    if final_voice is None:
                        final_voice = number_voice
                    else:
                        final_voice += number_voice
                elif item=="{emi_amount}":
                    entities["emi_amount"] = customer["emi_amt"]
                    number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                    if final_voice is None:
                        final_voice = number_voice
                    else:
                        final_voice += number_voice
                elif item=="{amount}":
                    entities["amount"] = customer["emi_amt"]
                    number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                    if final_voice is None:
                        final_voice = number_voice
                    else:
                        final_voice += number_voice
                elif item=="{partial_payment_amount}":
                    entities["partial_payment_amount"] = customer["emi_amt"]
                    number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                    if final_voice is None:
                        final_voice = number_voice
                    else:
                        final_voice += number_voice
                elif item=="{ptp_partial_amount}":
                    entities["ptp_partial_amount"] = customer["emi_amt"]
                    number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                    if final_voice is None:
                        final_voice = number_voice
                    else:
                        final_voice += number_voice
                elif item=="{total_emi}":
                        entities["total_emi"] = customer["emi_amt"]
                        number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                elif item=="{no_of_loans}":
                        entities["no_of_loans"] = customer["emi_amt"]
                        number_voice = hindi_number_processor.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                elif item == "{monthly_emi_date}":
                    entities["monthly_emi_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                        replace(year=2021).strftime("%d %B %Y")
                    date_voice = hindi_date_processor.get_recorded_voice_for_date(customer["emi_date"])
                    if final_voice is None:
                        final_voice = date_voice
                    else:
                        final_voice += date_voice
                elif item == "{ptp_day}":
                    entities["ptp_day"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                        replace(year=2021).strftime("%d %B %Y")
                    date_voice = hindi_date_processor.get_recorded_voice_for_date(customer["emi_date"])
                    if final_voice is None:
                        final_voice = date_voice
                    else:
                        final_voice += date_voice
                elif item == "{emi_date}":
                    print(customer["phone_number"])
                    entities["emi_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                        replace(year=2021).strftime("%d %B %Y")
                    date_voice = hindi_date_processor.get_recorded_voice_for_date(customer["emi_date"])
                    if final_voice is None:
                        final_voice = date_voice
                    else:
                        final_voice += date_voice
                elif item == "{ptp_date}":
                    entities["ptp_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                        replace(year=2021).strftime("%d %B %Y")
                    date_voice = hindi_date_processor.get_recorded_voice_for_date(customer["emi_date"])
                    if final_voice is None:
                        final_voice = date_voice
                    else:
                        final_voice += date_voice
            else:
                # item = item.strip().encode('utf-8')
                print(item)
                if item == "ko":
                    item = "को"
                hash_object = hashlib.md5(item.encode('utf-8'))
                file_name = str(hash_object.hexdigest())
                if file_name + ".wav" in os.listdir("../avail_finance/hindi/entity"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav("../avail_finance/hindi/entity/{}.wav".format(file_name))
                    else:
                        final_voice += AudioSegment.from_wav("../avail_finance/hindi/entity/{}.wav".format(file_name))
                else:
                    raise ValueError("file name is not found {} and text is {}".format(file_name, item))

        if "ko" in response:
            response = response.replace("ko", "को")
        final_response = response.format(**entities)
        hash_object = hashlib.md5(final_response.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        print(final_response, file_name)
        if file_name not in final_entity_responses:
            final_entity_responses.append(file_name)
            if final_voice:
                final_voice.export("../avail_finance/hindi/static/{}.wav".format(file_name), format="wav")
        else:
            pass

now = datetime.datetime.now()

ptp_dates = []
for item in range(0, 60):
    date = now + datetime.timedelta(days=item)
    ptp_dates.append(date.strftime("%d-%m-%Y"))
print(ptp_dates)

for ptp_date in ptp_dates:
    for response in ptp_entities_responses:
        formatted_response = get_formatted_response(response)
        matches = re.findall(r"\{(.*?)\}", response)
        matches = ["{" + item + "}" for item in matches]
        final_voice = None
        entities = {}
        for item in formatted_response:
            if item in matches:
                item = item.replace("{", "")
                item = item.replace("}", "")
                entities[item] = datetime.datetime.strptime(ptp_date, "%d-%m-%Y"). \
                        strftime("%d %B %Y")
                date_voice = hindi_date_processor.get_recorded_voice_for_date(ptp_date)
                if final_voice is None:
                    final_voice = date_voice
                else:
                    final_voice += date_voice
            else:
                hash_object = hashlib.md5(item.encode('utf-8'))
                file_name = str(hash_object.hexdigest())
                if file_name + ".wav" in os.listdir("../avail_finance/hindi/entity"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav("../avail_finance/hindi/entity/{}.wav".format(file_name))
                    else:
                        final_voice += AudioSegment.from_wav("../avail_finance/hindi/entity/{}.wav".format(file_name))
                else:
                    raise ValueError("file name is not found {} and text is {}".format(file_name, item))
        final_response = response.format(**entities)
        hash_object = hashlib.md5(final_response.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        print(final_response)
        if file_name not in final_entity_responses:
            final_entity_responses.append(file_name)
            if final_voice:
                # print(file_name)
                final_voice.export("../avail_finance/hindi/static/{}.wav".format(file_name), format="wav")
        else:
            pass
# #
# #
