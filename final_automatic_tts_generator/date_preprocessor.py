import datetime
import os

from pydub import AudioSegment

dates = {}
for item in os.listdir("../motilal_responses/ORDINAL/ENGLISH"):
    file_name = "../motilal_responses/ORDINAL/ENGLISH/" + item
    dates[item] = AudioSegment.from_wav(file_name)

months = {}
for item in os.listdir("../motilal_responses/MONTHS/ENGLISH"):
    file_name = "../motilal_responses/MONTHS/ENGLISH/" + item
    item = item.lower()
    months[item] = AudioSegment.from_wav(file_name)


def get_recorded_voice_for_date(date):
    final = None
    formatted_date = datetime.datetime.strptime(date, "%d-%b")
    if str(formatted_date.day) + ".wav" in dates:
        if final is None:
            final = dates.get(str(formatted_date.day) + ".wav")
            # final = AudioSegment.from_wav(
            #     "../Navi_bot_responses/Variables/Ordinals/{}.wav".format(str(formatted_date.day)))
        else:
            final += dates.get(str(formatted_date.day) + ".wav")
            # final += AudioSegment.from_wav(
            #     "../Navi_bot_responses/Variables/Ordinals/{}.wav".format(str(formatted_date.day)))
            # print("working")
    else:
        print("---error", str(formatted_date.day))
        assert True
    month = formatted_date.strftime("%B").lower()
    if month + ".wav" in months:
        if final is None:
            final = months.get(month + ".wav")
            # final = AudioSegment.from_wav("../Navi_bot_responses/Variables/English/Months/{}.wav".format(month))
        else:
            final += months.get(month + ".wav")
            # final += AudioSegment.from_wav("../Navi_bot_responses/Variables/English/Months/{}.wav".format(month))
            print("working")
        # print(formatted_date.day)
    else:
        raise Exception("errror", str(formatted_date.month).lower())
        # print("errror", str(formatted_date.month).lower())
    # if final:
    #     final.export("formatted_dates/{}.mp3".format(date), format="mp3")
    return final
