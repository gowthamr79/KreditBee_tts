import datetime
import os
# from local_settings import CURRENT_PATH
from pydub import AudioSegment
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_recorded_voice_for_date(date):
    final = None
    formatted_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    if str(formatted_date.day) + ".wav" in os.listdir(CURRENT_PATH+"/avail_finance/KANNADA NUMBERS"):
        if final is None:
            final = AudioSegment.from_wav(
                CURRENT_PATH+"/avail_finance/KANNADA NUMBERS/{}.wav".format(str(formatted_date.day)))
        else:
            final += AudioSegment.from_wav(
                CURRENT_PATH+"/avail_finance/KANNADA NUMBERS/{}.wav".format(str(formatted_date.day)))
            # print("working")
    else:
        print("---error", str(formatted_date.day))
        assert True
    # month = str(formatted_date.month)
    month = formatted_date.strftime("%B")
    print(month)
    if month + ".wav" in os.listdir(CURRENT_PATH+"/avail_finance/KANNADA MONTHS"):
        if final is None:
            final = AudioSegment.from_wav(CURRENT_PATH+"/avail_finance/KANNADA MONTHS/{}.wav".format(month))
        else:
            final += AudioSegment.from_wav(CURRENT_PATH+"/avail_finance/KANNADA MONTHS/{}.wav".format(month))
            print("working")
        # print(formatted_date.day)
    else:
        raise Exception("errror", str(formatted_date.month).lower())
        # print("errror", str(formatted_date.month).lower())
    # if final:
    #     final.export("../formatted_dates/{}.wav".format(date), format="wav")
    return final

# while True:
#     x = input()
#     get_recorded_voice_for_date(x)