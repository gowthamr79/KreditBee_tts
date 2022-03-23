import datetime
import hashlib
import json
import os
import re
import requests
# from local_settings import CURRENT_PATH
from avail_finance_english_generator import number_preprocessing, date_preprocessor
from pydub import AudioSegment

import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root
sys.path.append(ROOT_DIR)


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
        if sub_string == ".":
            continue
        if sub_string!="":
            positon = response.find(sub_string)
            print("Position:",positon)
            positions[positon] = sub_string
    for item in sorted(positions):
        formatted_responses.append(positions[item])
    return formatted_responses


general_entities = ["monthly_emi","emi_amount","total_amount","amount","partial_payment_amount","ptp_partial_amount","total_emi","no_of_loans","ptp_day","emi_date","ptp_date","monthly_emi_date"]
entities_response = {}
static_response = {}
for item in os.listdir(CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/ENTITY/"):
    file_name = CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/ENTITY/" + item
    if file_name != CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/ENTITY/.DS_Store":
        entities_response[item] = AudioSegment.from_wav(file_name)
for item in os.listdir(CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/STATIC/"):
    file_name = CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/STATIC/" + item
    if file_name != CURRENT_PATH + "/KREDITBEE_converted/ENGLISH/STATIC/.DS_Store":
        static_response[item] = AudioSegment.from_wav(file_name)
# for item in os.listdir(CURRENT_PATH + "/avail_finance_american_accent"):
#     file_name = CURRENT_PATH + "/avail_finance_american_accent/" + item
#     if file_name != CURRENT_PATH + "/avail_finance_american_accent/.DS_Store":
#         static_response[item] = AudioSegment.from_wav(file_name)

with open("Sheet1.json", "r+", encoding='utf-8') as f:
    data = json.load(f)


def generate_tts_files_static(message):
    final_voice = None
    hash_object = hashlib.md5(message.encode('utf-8'))
    print("----------------", message)
    file_name = str(hash_object.hexdigest())
    print("File name:",file_name)
    if file_name + ".wav" in static_response:
        if final_voice is None:
            final_voice = static_response.get(file_name + ".wav")
        else:
            final_voice += static_response.get(file_name + ".wav")
    else:
        # downlaod_data=requests.get("https://calldataczentrix.blob.core.windows.net/cred-data/{}.wav".format(file_name))
        # if downlaod_data.status_code!=200:
        #     # return None
        raise ValueError("file name is not found {} and text is '{}'".format(file_name, message))
        # # else:
        # with open(CURRENT_PATH+"/avail_finance/english/static/{}.wav".format(file_name),"wb") as f:
        #     f.write(downlaod_data.content)
        # audio_voice=AudioSegment.from_wav(CURRENT_PATH+"/avail_finance/english/static/{}.wav".format(file_name))
        # item=file_name+".wav"
        # static_response[item] = audio_voice
        # if final_voice is None:
        #     final_voice=audio_voice
        # else:
        #     final_voice+=audio_voice
    # final_voice = final_voice.set_frame_rate(8000)
    # final_voice.export("test2.wav", format="wav", bitrate="32k")
    return final_voice


def generate_tts_files_dynamic(utterance, message):
    final_voice = None
    print("Utterance:",utterance)
    formatted_responses = get_formatted_response(utterance)
    print("Formatted Response:",formatted_responses)
    _entities = []
    for _response in formatted_responses:
        if "{" in _response:
            _entities.append(_response.replace("{", "").replace("}", ""))
        else:
            print("*******",_response)
            message = message.replace(_response, "-")
            print("New: ",message)
    message = message.split("-")
    print("Message:",message)
    formatted_values = []
    for _item in message:
        if _item:
            _item = _item.replace(".", "")
            _item = _item.strip()
            formatted_values.append(_item)
    entities = dict(zip(_entities, formatted_values))
    print("Entities:",entities)
    for response in formatted_responses:
        if "{" in response:
            response = response.replace("{", "").replace("}", "")
            if response.lower() == "emi_amount" or response.lower() == "monthly_emi" or response.lower()== "amount" or \
                response.lower()== "partial_payment_amount" or response.lower()== "ptp_partial_amount" or response.lower()=="total_emi" or response.lower()=="no_of_loans" or response.lower()=="total_amount":
                number_voice = number_preprocessing.get_recorded_voice_for_number(entities[response])
                if final_voice is None:
                    final_voice = number_voice
                else:
                    final_voice += number_voice
            if response.lower() == "due_date" or response.lower() == "given_date" or response.lower() == "ptp_day" or response.lower() == "monthly_emi_date" or \
                response.lower()== "emi_date" or response.lower()== "ptp_date" or response.lower()== "monthly_emi_date":
                value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d-%m-%Y")
                date_voice = date_preprocessor.get_recorded_voice_for_date(value)
                if final_voice is None:
                    final_voice = date_voice
                else:
                    final_voice += date_voice
        else:
            hash_object = hashlib.md5(response.encode('utf-8'))
            file_name = str(hash_object.hexdigest())
            if file_name + ".wav" in entities_response:
                if final_voice is None:
                    final_voice = entities_response.get(file_name + ".wav")
                else:
                    final_voice += entities_response.get(file_name + ".wav")
            else:
                raise ValueError("file name is not found {} and text is '{}'".format(file_name, response))
    return final_voice


def classify_static_dynamic_template(message, utterance_name):
    for item in data:
        if item['Response_ID'] == utterance_name:
            if item['English']!="":
                utterance=item['English']
            if '{' in utterance and '}' in utterance:
                if '{day_time}' not in utterance:
                    return generate_tts_files_dynamic(utterance, message)
                else:
                    return generate_tts_files_static(message)
            else:
                return generate_tts_files_static(message)
# def classify_static_dynamic_template(message, utterance_name):
#     for item in data:
#         if item['Utterance Template'] == utterance_name:
#             utterance=item['responses']
#             # if '{' in utterance and '}' in utterance:
#             #     if '{day_time}' not in utterance:
#             #         return generate_tts_files_dynamic(utterance, message)
#             #     else:
#             #         return generate_tts_files_static(message)
#             # else:
#             return generate_tts_files_static(utterance)
# classify_static_dynamic_template(
#     message="Yes, I'm listening.",
#     utterance_name="utter_greet_again")
