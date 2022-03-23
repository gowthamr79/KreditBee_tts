import datetime
import hashlib
import json
import os
import re
# from local_settings import CURRENT_PATH
from avail_finance_kannada_tts_generator import kannada_number_processor, kannada_date_processor
from pydub import AudioSegment

import os, sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("e322",ROOT_DIR)
sys.path.append(ROOT_DIR)


# print("******",sys.path)


def get_formatted_response(response):
    matches = re.findall(r"\{(.*?)\}", response)
    matches = ["{" + item + "}" for item in matches]
    split_regex = ""
    for item in range(len(matches)):
        if item != len(matches) - 1:
            split_regex += matches[item] + " | "
        else:
            split_regex += matches[item]
    sub_strings = re.split(split_regex, response)
    if "" in sub_strings:
        sub_strings.remove("")
    sub_strings.extend(matches)
    positions = {}
    formatted_responses = []
    for sub_string in sub_strings:
        if sub_string == ".":
            continue
        positon = response.find(sub_string)
        positions[positon] = sub_string
    for item in sorted(positions):
        formatted_responses.append(positions[item])
    # print("Formatted Response:",formatted_responses)
    return formatted_responses


general_entities = ["emi_amount", "due_date"]
entities_response = {}
static_response = {}
for item in os.listdir(CURRENT_PATH + "/KREDITBEE_converted/KANNADA/ENTITY/"):
    # print("******", item)
    file_name = CURRENT_PATH + "/KREDITBEE_converted/KANNADA/ENTITY/" + item
    if file_name != CURRENT_PATH + "/KREDITBEE_converted/KANNADA/ENTITY/.DS_Store":
        entities_response[item] = AudioSegment.from_wav(file_name)
for item in os.listdir(CURRENT_PATH + "/KREDITBEE_converted/KANNADA/STATIC/"):
    # print("******", item)
    file_name = CURRENT_PATH + "/KREDITBEE_converted/KANNADA/STATIC/" + item
    if file_name != CURRENT_PATH + "/KREDITBEE_converted/KANNADA/STATIC/.DS_Store":
        static_response[item] = AudioSegment.from_wav(file_name)

with open(CURRENT_PATH + "/Sheet1.json", "r+") as f:
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
def generate_tts_files_static(message=None, template_name=None):
    final_voice = None
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
        raise ValueError("file name is not found {} and text is {}".format(file_name, message))
    # final_voice = final_voice.set_frame_rate(8000)
    # final_voice.export("test2.wav", format="wav", bitrate="32k")
    return final_voice


def generate_tts_files_dynamic(utterance, message):
    final_voice = None
    if "\\u200c" in message:
        message = message.replace("\\u200c", '\u200c')
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
            if response == "emi_amount" or response == "monthly_emi" or response == "EMI_Amount" or response == "no_of_loans":
                number_voice = kannada_number_processor.get_recorded_voice_for_number(entities[response])
                # number_voice.export("{}.wav", format="wav")
                if final_voice is None:
                    final_voice = number_voice
                else:
                    final_voice += number_voice
            if response == "due_date" or response == "EMI_Date" or response == "given_date" or response == "ptp_day" or response == "monthly_emi_date":
                value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d-%m-%Y")
                date_voice = kannada_date_processor.get_recorded_voice_for_date(value)
                # date_voice.export("{}.wav".format(value), format="wav")
                if final_voice is None:
                    final_voice = date_voice
                else:
                    final_voice += date_voice
        else:
            hash_object = hashlib.md5(response.strip().encode('utf-8'))
            file_name = str(hash_object.hexdigest())
            if file_name + ".wav" in entities_response:
                if final_voice is None:
                    final_voice = entities_response.get(file_name + ".wav")
                    # final_voice = AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
                else:
                    final_voice += entities_response.get(file_name + ".wav")
                    # final_voice += AudioSegment.from_wav("../Navi_bot_responses/english/entity/{}.wav".format(file_name))
            else:
                raise ValueError("file name is not found {} and text is {}".format(file_name, response))
    # final_voice = final_voice.set_frame_rate(8000)
    # final_voice.export("test1.wav", format="wav", bitrate="32k")
    return final_voice


def classify_static_dynamic_template(message, utterance_name):
    for item in data:
        if item['Response_ID'] == utterance_name:
            utterance = item['Kannada']
            if '{' in utterance and '}' in utterance:
                if '{day_time}' not in utterance:
                    # print("Dynamic template")
                    return generate_tts_files_dynamic(utterance, message)
                else:
                    # print("Static Template")
                    return generate_tts_files_static(message)
            else:
                # print("Static Template")
                return generate_tts_files_static(message)
# classify_static_dynamic_template(
#     message="ನಿಮ್ಮ ಮಾಸಿಕ ನಿಗದಿತ ಮೊತ್ತ 879 ಬಾಕಿ ಇದೆ. ನಿಮ್ಮ ಮಾಸಿಕ ಪಾವತಿ ದಿನಾಂಕ 16 July 2021",
#     utterance_name="utter_inform_reminder")

# I’m sending you a payment link on SMS amounting to Rs. {monthly_emi}.
# I’m sending you a payment link on SMS amounting to Rs. 524
