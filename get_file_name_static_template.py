import os

from sample1 import find_hash
import json
import subprocess

with open("new_response.json", "r") as f:
    bot_responses = json.load(f)
out_file = open("missing_template.txt", "w")


def get_hash_name(text):
    if "{" not in text:
        template, file_name = find_hash(text)
        if text == "क्षमा करें। मैं आपकी बात समझ नहीं पाया।":
            print("adssaf", file_name, template)
        print(file_name, template)
        if file_name + ".wav" not in os.listdir("avail_finance/hindi/static"):
            print(file_name, template)
            out_file.write(template + "\t" + file_name + "\n")

        # name_exist = subprocess.Popen(
        #     "find /Users/debadityamandal/Desktop/motilal-tts-generate -name " + file_name + ".wav", shell=True,
        #     stdout=subprocess.PIPE)
        # if len(name_exist.stdout.read()) == 0:
        #     out_file.write(template + "\t" + file_name + "\n")


for row in bot_responses:
    # get_hash_name(row["English Utterance"])
    if row["Utterance Template"] == "utter_inform_cibil_score":
        print("sdfsdf")
    get_hash_name(row["English Utterance"])
    # get_hash_name(row["Kannada Responses"])
