import datetime
import hashlib
import json
import os
import re

import number_preprocessing
import date_preprocessor
from pydub import AudioSegment

import os, sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
print("e322",ROOT_DIR)
sys.path.append(ROOT_DIR)
print(sys.path)


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
    # print(formatted_responses)
    return formatted_responses


general_entities = ["emi_amount", "due_date"]
entities_response = {}
for item in os.listdir("../Navi_bot_responses/english/entity"):
    file_name = "../Navi_bot_responses/english/entity/" + item
    if file_name != "../Navi_bot_responses/english/entity/.DS_Store":
        entities_response[item] = AudioSegment.from_wav(file_name)

with open("../Navi_responses.json", "r+") as f:
    data = json.load(f)


def generate_tts_files(message=None, utterance_name=None):

    _message = message
    utterance = 'English Utterance'
    print(utterance.find("English") + len("English"))
    final_voice = None
    for item in data:
        if item and "Utterance Name" in item and item["Utterance Name"] == utterance_name and \
                utterance in item:
            # print(item[utterance], message)
            # print(get_formatted_response(item[utterance]))
            formatted_responses = get_formatted_response(item[utterance])
            _entities = []
            for _response in formatted_responses:
                if "{" in _response:
                    _entities.append(_response.replace("{", "").replace("}", ""))
                else:
                    message = message.replace(_response, "-")
            message = message.split("-")
            # print(_entities)
            formatted_values = []
            for _item in message:
                if _item:
                    _item = _item.replace(".", "")
                    _item = _item.strip()
                    formatted_values.append(_item)
            entities = dict(zip(_entities, formatted_values))
            # print("3245675t4re",entities)
            for response in formatted_responses:
                if "{" in response:
                    response = response.replace("{", "").replace("}", "")
                    if response == "emi_amount":
                        number_voice = number_preprocessing.get_recorded_voice_for_number(entities[response])
                        # number_voice.export("{}.wav", format="wav")
                        if final_voice is None:
                            final_voice = number_voice
                        else:
                            final_voice += number_voice
                    if response == "due_date" or response == "given_date" or response == "end_date":
                        value = datetime.datetime.strptime(entities[response], "%d %B %Y").strftime("%d-%m-%Y")
                        date_voice = date_preprocessor.get_recorded_voice_for_date(value)
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
                        raise ValueError("file name is not found {} and text is {}".format(file_name, item))
            # final_voice = final_voice.set_frame_rate(8000)
            # final_voice.export("test1.wav", format="wav", bitrate="32k")
            return final_voice

#
# generate_tts_files(message="As per your promise, please make the payment before 07 June 2021. May you've a great day!",
#                    utterance_name="utter_first_case_inform_payment_date")
