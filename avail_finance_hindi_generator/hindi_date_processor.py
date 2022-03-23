import datetime
import os, sys
# from pydub import AudioSegment
from pydub import AudioSegment
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root
# print("e322",ROOT_DIR)
sys.path.append(CURRENT_PATH)


def get_recorded_voice_for_date(date):
    final = None
    formatted_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    if str(formatted_date.day) + ".wav" in os.listdir(CURRENT_PATH+"/motilal_responses/NUMBERS/HINDI"):
        if final is None:
            final = AudioSegment.from_wav(
                CURRENT_PATH+"/motilal_responses/NUMBERS/HINDI/{}.wav".format(str(formatted_date.day)))
        else:
            final += AudioSegment.from_wav(
                CURRENT_PATH+"/motilal_responses/NUMBERS/HINDI/{}.wav".format(str(formatted_date.day)))
            # print("working")
    else:
        print("---error", str(formatted_date.day))
        assert True
    # month = str(formatted_date.month)
    month = formatted_date.strftime("%B").upper()
    print(month)
    if month + ".wav" in os.listdir(CURRENT_PATH+"/motilal_responses/MONTHS/HINDI"):
        if final is None:
            final = AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/MONTHS/HINDI/{}.wav".format(month))
        else:
            final += AudioSegment.from_wav(CURRENT_PATH+"/motilal_responses/MONTHS/HINDI/{}.wav".format(month))
            print("working")
        # print(formatted_date.day)
    else:
        raise Exception("errror", str(formatted_date.month).lower())
        # print("errror", str(formatted_date.month).lower())
    # if final:
    #     final.export(CURRENT_PATH+"/formatted_dates/{}.wav".format(date), format="wav")
    return final

# while True:
#     x = input()
#     get_recorded_voice_for_date(x)