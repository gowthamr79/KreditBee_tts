import hashlib
import json
import os
import re

def find_hash(text):
    template = text
    hash_object = hashlib.md5(template.encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    return template, file_name

with open("bot_responses.json","r") as f:
    data=json.load(f)

# PATH="/home/azureuser/cred-tts/CRED NEW RESPONSES/ENGLISH/"
# for file in os.listdir(PATH):
#     file_name=file.split(".")[0]
#     for row in data:
#         if row['Template']==file_name:
#             text=row['Hindi']
#             template,updated_file_name=find_hash(text)
#             os.rename(PATH+file_name+".wav",PATH+updated_file_name+".wav")
# print("completed")
# f=open("file_names.txt","w+")
# PATH="/home/azureuser/cred-tts/CRED VOX/HINDI/ENTITY/"
# for file in os.listdir(PATH):
#     file_name=file.split(".")[0]
#     for row in data:
#         if row['Template'].lower()==file_name.lower():
#             text=row['English']
#             template,updated_file_name=find_hash(text)
#             os.rename(PATH+file_name+".wav",PATH+updated_file_name+".wav")

# for file in os.listdir(PATH):
#     file_name=file.split(".")[0]
#     for row in data:
#         if row['Template'].lower()==file_name.lower():
#             text=row['Hindi']
#             template,updated_file_name=find_hash(text)
#             os.rename(PATH+file_name+".wav",PATH+updated_file_name+".wav")
# print("Completed")

# for row in data:
#     if "{" in row['English']:
#         english=row["English"]
#         splits=re.split(r"\{(.*?)\}",english)
#         print("Splits:",splits)
#         for shell in splits:
#             if "{" not in shell:
#                 template,file_name=find_hash(shell)
#                 f.write('"'+template+'"'+"\t"+file_name+"\n")
#     else:
#         if "{" in row['English Utterance current']:
#             english=row["English Utterance current"]
#             splits=re.split(r"\{(.*?)\}",english)
#             print("Splits1:",splits)
#             for shell in splits:
#                 if "{" not in shell:
#                     template,file_name=find_hash(shell)
#                     f.write('"'+template+'"'+"\t"+file_name+"\n")
#     if "{" in row['Hindi Responses updated (ankit-rakesh']:
#         hindi=row['Hindi Responses updated (ankit-rakesh']
#         splits=re.split(r"\{(.*?)\}",hindi)
#         print("Splits2:",splits)
#         for shell in splits:
#             if "{" not in shell:
#                 template,file_name=find_hash(shell)
#                 f.write('"'+template+'"'+"\t"+file_name+"\n")
# f.close()

# 1279199da499d0a1a54551629897ae39
# क्या आप इस कॉल के दौरान भुगतान कर सकते हैं? a4105dbf21accf13c4b4b5c227327a66
# would like to continue in the English language 018077c93424cfc304a76172b1e7880d
#                                                01807c93424cfc304a76172b1e7880d.wav
# क्या आप हिंदी में बात करना चाहेंगे 6e7488d055ea935414d24f9f8ff747e2
# 011df9f834dfb11f05329e6bef90fcf2
# a3c3ffe6c7eea7bffe83bf07197f70c7
# a3c3ffe6c7eea7bffe83bf07197f70c7
# /d390048682b3e66a9f996f4483aab230
# fe52b750ea98c699083bf801b7bde087
# aa3552a616aeefcbe3a64dce54850e4b
#54ffeededb255dd96bb9216c89c17ed8
#b4afd75fd559998ed24a370a4e6c01b5

print(find_hash("অবশ্যই,আমি অপেক্ষা করছি।"))