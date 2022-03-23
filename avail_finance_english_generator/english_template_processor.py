import datetime
import hashlib
import json
import os
import re

from pydub import AudioSegment

import date_preprocessor
import number_preprocessing
import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
print("e322",CURRENT_PATH)
sys.path.append(CURRENT_PATH)
print(sys.path)
with open("../bot_responses.json", "r+") as f:
    data = json.load(f)

with open("../customer_details_english.json", "r+") as f:
    customer_details = json.load(f)
# print(customer_details)

general_entities_responses = []
ptp_entities_responses = []

general_entities = ["monthly_emi","emi_amount","amount","partial_payment_amount","ptp_partial_amount","total_emi","no_of_loans"]
ptp_entities = ["ptp_day","emi_date","ptp_date","monthly_emi_date"]
for item in data:
    text=item['English']
    matches = re.findall(r"\{(.*?)\}", text)
    if matches:
        for match in matches:
            if match in general_entities:
                if text not in general_entities_responses:
                    general_entities_responses.append(text)
            if match in ptp_entities:
                if text not in ptp_entities_responses:
                    ptp_entities_responses.append(text)


print(general_entities_responses)
print(ptp_entities_responses)


def get_formatted_response(response):
    matches = re.findall(r"\{(.*?)\}", response)
    matches = ["{" + item + "}" for item in matches]
    split_regex = ""
    for item in range(len(matches)):
        if item != len(matches) - 1:
            split_regex += matches[item] + "|"
        else:
            split_regex += matches[item]
    sub_strings = re.split(split_regex, response)
    sub_strings.extend(matches)
    positions = {}
    formatted_responses = []
    for sub_string in sub_strings:
        if sub_string == "." or sub_string == "":
            continue
        positon = response.find(sub_string)
        positions[positon] = sub_string
    for item in sorted(positions):
        formatted_responses.append(positions[item])
    # print(formatted_responses)
    return formatted_responses


final_entity_responses = []


for customer in customer_details:
    # if "custom_field_2" in customer and customer["custom_field_2"] == "hi":
        for response in general_entities_responses:
            # response = response.replace(".", "")
            print(response)
            matches = re.findall(r"\{(.*?)\}", response)
            matches = ["{" + item + "}" for item in matches]
            formatted_response = get_formatted_response(response)
            print(formatted_response)
            final_voice = None
            entities = {}
            for item in formatted_response:
                if item in matches:
                    if item == "{monthly_emi}":
                        entities["monthly_emi"] = customer["emi_amt"]
                        print("customer phonenumber:",customer["phone_number"])
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{emi_amount}":
                        entities["emi_amount"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{amount}":
                        entities["amount"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{partial_payment_amount}":
                        entities["partial_payment_amount"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{ptp_partial_amount}":
                        entities["ptp_partial_amount"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{total_emi}":
                        entities["total_emi"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    elif item=="{no_of_loans}":
                        entities["no_of_loans"] = customer["emi_amt"]
                        number_voice = number_preprocessing.get_recorded_voice_for_number(customer["emi_amt"])
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    if item == "{monthly_emi_date}":
                        entities["monthly_emi_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                            replace(year=2021).strftime("%d %B %Y")
                        date_voice = date_preprocessor.get_recorded_voice_for_date(customer["emi_date"])
                        if final_voice is None:
                            final_voice = date_voice
                        else:
                            final_voice += date_voice
                    elif item == "{ptp_day}":
                        entities["ptp_day"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                            replace(year=2021).strftime("%d %B %Y")
                        date_voice = date_preprocessor.get_recorded_voice_for_date(customer["emi_date"])
                        if final_voice is None:
                            final_voice = date_voice
                        else:
                            final_voice += date_voice
                    elif item == "{emi_date}":
                        print("'%s'"%customer["emi_date"])
                        entities["emi_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                            replace(year=2021).strftime("%d %B %Y")
                        date_voice = date_preprocessor.get_recorded_voice_for_date(customer["emi_date"])
                        if final_voice is None:
                            final_voice = date_voice
                        else:
                            final_voice += date_voice
                    elif item == "{ptp_date}":
                        entities["ptp_date"] = datetime.datetime.strptime(customer["emi_date"], "%d-%m-%Y").\
                            replace(year=2021).strftime("%d %B %Y")
                        date_voice = date_preprocessor.get_recorded_voice_for_date(customer["emi_date"])
                        if final_voice is None:
                            final_voice = date_voice
                        else:
                            final_voice += date_voice

                else:
                    # print(item.strip())
                    hash_object = hashlib.md5(item.encode('utf-8'))
                    file_name = str(hash_object.hexdigest())
                    # print(file_name)
                    if file_name + ".wav" in os.listdir("../avail_finance/english/entity"):
                        if final_voice is None:
                            final_voice = AudioSegment.from_wav("../avail_finance/english/entity/{}.wav".format(file_name))
                        else:
                            final_voice += AudioSegment.from_wav("../avail_finance/english/entity/{}.wav".format(file_name))
                    else:
                        # if file_name not in ["7fa50e1e9219e858600d9c4be98f7a00", "25b53bf9278279f36373c087b9302b6f"]:
                        # if file_name != "7fa50e1e9219e858600d9c4be98f7a00" or file_name != "25b53bf9278279f36373c087b9302b6f":
                        raise ValueError("file name is not found {} and text is '{}'".format(file_name, item))

            final_response = response.format(**entities)
            hash_object = hashlib.md5(final_response.encode('utf-8'))
            file_name = str(hash_object.hexdigest())
            print(final_response, file_name)
            if file_name not in final_entity_responses:
                final_entity_responses.append(file_name)
                if final_voice:
                    final_voice.export("../avail_finance/english/static/{}.wav".format(file_name), format="wav")
            else:
                pass

# greet = AudioSegment.from_wav(CURRENT_PATH+"/avail_finance/english/entity/utter_greet.wav")
# # greet1=AudioSegment.from_wav(CURRENT_PATH+"/temporary_files/AVAIL ADDITIONAL ENGLISH.wav")
# good_morning = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good morning.wav") + greet
# # good_morning_1 = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good morning.wav") + greet1
# good_evening = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good evening.wav") + greet
# # good_evening_1 = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good evening.wav") + greet1
# good_afternoon = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good aftrenoon.wav") + greet
# # good_afternoon_1 = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/GREETINGS/Good aftrenoon.wav") + greet1

# greetings = ["good morning", "good afternoon", "good evening"]
# for item in data:
#     if item["Utterance Template"] == "utter_greet":
#         template = item["English Utterance"]
#         for _item in greetings:
#             template = item["English Utterance"]
#             template = template.format(day_time=_item)
#             hash_object = hashlib.md5(template.encode('utf-8'))
#             file_name = str(hash_object.hexdigest())
#             print(template, file_name)
#             if _item == "good morning":
#                 good_morning.export("../avail_finance/english/static/{}.wav".format(file_name), format="wav")
#             if _item == "good afternoon":
#                 good_afternoon.export("../avail_finance/english/static/{}.wav".format(file_name), format="wav")
#             if _item == "good evening":
#                 good_evening.export("../avail_finance/english/static/{}.wav".format(file_name), format="wav")

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
                date_voice = date_preprocessor.get_recorded_voice_for_date(ptp_date)
                if final_voice is None:
                    final_voice = date_voice
                else:
                    final_voice += date_voice
            else:
                hash_object = hashlib.md5(item.encode('utf-8'))
                file_name = str(hash_object.hexdigest())
                if file_name + ".wav" in os.listdir("../avail_finance/english/entity/"):
                    if final_voice is None:
                        final_voice = AudioSegment.from_wav("../avail_finance/english/entity/{}.wav".format(file_name))
                    else:
                        final_voice += AudioSegment.from_wav("../avail_finance/english/entity/{}.wav".format(file_name))
                else:
                    raise ValueError("file name is not found {} and text is '{}'".format(file_name, item))
        final_response = response.format(**entities)
        hash_object = hashlib.md5(final_response.encode('utf-8'))
        file_name = str(hash_object.hexdigest())
        print(final_response, file_name)
        if file_name not in final_entity_responses:
            final_entity_responses.append(file_name)
            if final_voice:
                final_voice.export("../avail_finance/english/static/{}.wav".format(file_name), format="wav")
        else:
            pass
        # print(formatted_response, response)
