import datetime
import hashlib
import json
import re
import requests
# from local_settings import CURRENT_PATH
import os, sys

CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root
# print("e322",ROOT_DIR)
sys.path.append(CURRENT_PATH)

from avail_finance_hindi_generator import hindi_number_processor,hindi_date_processor
from pydub import AudioSegment


# print("******",sys.path)


# def get_formatted_response(response):
#     matches = re.findall(r"\{(.*?)\}", response)
#     matches = ["{" + item + "}" for item in matches]
#     print("Matches:",matches)
#     split_regex = ""
#     for item in range(len(matches)):
#         if item != len(matches) - 1:
#             split_regex += matches[item] + " | "
#         else:
#             split_regex += matches[item]
#     print(split_regex)
#     sub_strings = re.split(split_regex, response)
#     sub_strings.extend(matches)
#     print(sub_strings)
#     positions = {}
#     formatted_responses = []
#     print(response)
#     for sub_string in sub_strings:
#         if sub_string == ".":
#             continue
#         positon = response.find(sub_string)
#         print(sub_string)
#         print("Word: %s and position: %d"%(sub_string,positon))
#         positions[positon] = sub_string
#     print(positions)
#     for item in sorted(positions):
#         formatted_responses.append(positions[item])
#     # print("Formatted Response:",formatted_responses)
#     return formatted_responses

def get_formatted_response(response):
    # print("Response:",response)
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
    # print(splitted)
    return splitted

general_entities = ["monthly_emi","emi_amount","total_amount","amount","partial_payment_amount","ptp_partial_amount","total_emi","no_of_loans","ptp_day","emi_date","ptp_date","monthly_emi_date"]
entities_response = {}
static_response={}
for item in os.listdir(CURRENT_PATH+"/KREDITBEE_converted/HINDI/ENTITY/"):
    # print("******", item)
    file_name = CURRENT_PATH+"/KREDITBEE_converted/HINDI/ENTITY/" + item
    if file_name != CURRENT_PATH+"/KREDITBEE_converted/HINDI/ENTITY/.DS_Store":
        entities_response[item] = AudioSegment.from_wav(file_name)
for item in os.listdir(CURRENT_PATH+"/KREDITBEE_converted/HINDI/STATIC/"):
    # print("******", item)
    file_name = CURRENT_PATH+"/KREDITBEE_converted/HINDI/STATIC/" + item
    if file_name != CURRENT_PATH+"/KREDITBEE_converted/HINDI/STATIC/.DS_Store":
        static_response[item] = AudioSegment.from_wav(file_name)

with open(CURRENT_PATH+"/Sheet1.json", "r+",encoding='utf-8') as f:
    data = json.load(f)


# def generate_tts_files(message=None, utterance_name=None):
#     _message = message
#     utterance = 'English Utterance'
#     # print(utterance.find("English") + len("English"))
#     final_voice = None
#     for item in data:
#         # print(item)
#         if item and "Utterance Template" in item and item["Utterance Template"] == utterance_name and \
#                 utterance in item:
#             # print(item[utterance], message)
#             # print(get_formatted_response(item[utterance]))
#             formatted_responses = get_formatted_response(item[utterance])
#             _entities = []
#             for _response in formatted_responses:
#                 if "{" in _response:
#                     _entities.append(_response.replace("{", "").replace("}", ""))
#                 else:
#                     message = message.replace(_response, "-")
#             message = message.split("-")
#             # print(_entities)
#             print(message)
#             formatted_values = []
#             for _item in message:
#                 if _item:
#                     print(_item)
#                     _item = _item.replace(".", "")
#                     _item = _item.strip()
#                     formatted_values.append(_item)
#             entities = dict(zip(_entities, formatted_values))
#             print(entities)
#             print(formatted_responses)
#             for response in formatted_responses:
#                 # print("********", response)
#                 if "{" in response:
#                     print(response)
#                     response = response.replace("{", "").replace("}", "")
#                     if response == "emi_amount" or response == "monthly_emi":
#                         number_voice = number_preprocessing.get_recorded_voice_for_number(entities[response])
#                         # number_voice.export("{}.wav", format="wav")
#                         if final_voice is None:
#                             final_voice = number_voice
#                         else:
#                             final_voice += number_voice
#                     if response == "due_date" or response == "given_date" or response == "end_date" or response == "monthly_emi_date":
#                         value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d-%m-%Y")
#                         date_voice = date_preprocessor.get_recorded_voice_for_date(value)
#                         # date_voice.export("{}.wav".format(value), format="wav")
#                         if final_voice is None:
#                             final_voice = date_voice
#                         else:
#                             final_voice += date_voice
#                 else:
#                     hash_object = hashlib.md5(response.strip().encode('utf-8'))
#                     file_name = str(hash_object.hexdigest())
#                     if file_name + ".wav" in entities_response:
#                         if final_voice is None:
#                             final_voice = entities_response.get(file_name + ".wav")
#                             # final_voice = AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
#                         else:
#                             final_voice += entities_response.get(file_name + ".wav")
#                             # final_voice += AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
#                     else:
#                         raise ValueError("file name is not found {} and text is {}".format(file_name, item))
#             final_voice = final_voice.set_frame_rate(8000)
#             final_voice.export("test1.wav", format="wav", bitrate="32k")
#             return final_voice
def generate_tts_files_static(message):
    final_voice=None
    hash_object = hashlib.md5(message.encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    if file_name + ".wav" in static_response:
        if final_voice is None:
            final_voice = static_response.get(file_name + ".wav")
            # final_voice = AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
        else:
            final_voice += static_response.get(file_name + ".wav")
            # final_voice += AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
    else:
        # downlaod_data=requests.get("https://calldataczentrix.blob.core.windows.net/cred-data/{}.wav".format(file_name))
        # if downlaod_data.status_code!=200:
        #     # return None
        raise ValueError("file name is not found {} and text is '{}'".format(file_name, message))
        # # else:
        # with open(CURRENT_PATH+"/avail_finance/hindi/static/{}.wav".format(file_name),"wb") as f:
        #     f.write(downlaod_data.content)
        # audio_voice=AudioSegment.from_wav(CURRENT_PATH+"/avail_finance/hindi/static/{}.wav".format(file_name))
        # item=file_name+".wav"
        # static_response[item] = audio_voice
        # if final_voice is None:
        #     final_voice=audio_voice
        # else:
        #     final_voice+=audio_voice
    # final_voice = final_voice.set_frame_rate(8000)
    # final_voice.export("test2.wav", format="wav", bitrate="32k")
    return final_voice
def generate_tts_files_dynamic(utterance,message):
    final_voice = None
    formatted_responses = get_formatted_response(utterance)
    _entities = []
    for _response in formatted_responses:
        if "{" in _response:
            _entities.append(_response.replace("{", "").replace("}", ""))
        else:
            message = message.replace(_response, "-")
    message = message.split("-")
    # print(_entities)
    # print(message)
    formatted_values = []
    for _item in message:
        if _item:
            # print(_item)
            _item = _item.replace(".", "")
            _item = _item.strip()
            formatted_values.append(_item)
    entities = dict(zip(_entities, formatted_values))
    # print(entities)
    # print(formatted_responses)
    for response in formatted_responses:
        # print("********", response)
        if "{" in response:
            # print(response)
            response = response.replace("{", "").replace("}", "")
            if response.lower() == "emi_amount" or response == "EMI_Amount" or response.lower() == "monthly_emi" or response.lower()== "amount" or \
                response.lower()== "partial_payment_amount" or response.lower()== "ptp_partial_amount" or response.lower()=="total_emi" or response.lower()=="no_of_loans" or response.lower()=="total_amount":
                number_voice = hindi_number_processor.get_recorded_voice_for_number(entities[response])
                if final_voice is None:
                    final_voice = number_voice
                else:
                    final_voice += number_voice
            if response.lower() == "due_date" or response.lower() == "given_date" or response.lower() == "ptp_day" or response.lower() == "monthly_emi_date" or \
                response.lower()== "emi_date" or response.lower()== "ptp_date" or response.lower()== "monthly_emi_date":
                value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d-%m-%Y")
                date_voice = hindi_date_processor.get_recorded_voice_for_date(value)
                if final_voice is None:
                    final_voice = date_voice
                else:
                    final_voice += date_voice
        else:
            hash_object = hashlib.md5(response.encode('utf-8'))
            file_name = str(hash_object.hexdigest())
            if file_name + ".wav" in entities_response:
                if final_voice is None:
                    print("*****",file_name+".wav")
                    final_voice = entities_response.get(file_name + ".wav")
                    # final_voice = AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
                else:
                    print("++++",file_name+".wav")
                    final_voice += entities_response.get(file_name + ".wav")
                    # final_voice += AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
            else:
                raise ValueError("file name is not found {} and text is '{}'".format(file_name, response))
    # final_voice = final_voice.set_frame_rate(8000)
    # final_voice.export("test1.wav", format="wav", bitrate="32k")
    return final_voice

def classify_static_dynamic_template(message,utterance_name):
    for item in data:
        if item['Response_ID']==utterance_name:
            utterance=item['Hindi']
            if '{' in utterance and '}' in utterance:
                if '{day_time}' not in utterance:
                    # print("Dynamic template")
                    return generate_tts_files_dynamic(utterance,message)
                else:
                    # print("Static Template")
                    return generate_tts_files_static(message)
            else:
                # print("Static Template")
                return generate_tts_files_static(message)
# print(classify_static_dynamic_template(
#     message="नमस्ते, मैं क्रेड से कॉल कर रही हूँ।आपकी 1897 रुपये की ईएमआई पेमेंट 12 November 2021 से बाकी है.",
#     utterance_name="utter_greet_cred"))

# I’m sending you a payment link on SMS amounting to Rs. {monthly_emi}.
# I’m sending you a payment link on SMS amounting to Rs. 524
