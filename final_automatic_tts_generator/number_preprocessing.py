import os

from num2words import num2words
from pydub import AudioSegment


def text2int(textnum, numwords=None):
    if numwords is None:
        numwords = {}
    if "" in textnum:
        textnum = textnum.replace("-", " ")
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

thousands = {}
hundreds = {}
singles = {}
for item in os.listdir("../motilal_responses/THOUSAND/ENGLISH"):
    file_name = "../motilal_responses/THOUSAND/ENGLISH/" + item
    thousands[item] = AudioSegment.from_wav(file_name)

for item in os.listdir("../motilal_responses/HUNDREDS/ENGLISH"):
    file_name = "../motilal_responses/HUNDREDS/ENGLISH/" + item
    hundreds[item] = AudioSegment.from_wav(file_name)
# print(thousands)

for item in os.listdir("../motilal_responses/NUMBERS/ENGLISH"):
    file_name = "../motilal_responses/NUMBERS/ENGLISH/" + item
    singles[item] = AudioSegment.from_wav(file_name)
# print(thousands)
# print(hundreds)
# print(singles)


def get_recorded_voice_for_number(number):
    raw_number = number
    number = num2words(number)
    number = number.replace("and", ",")
    number = number.split(",")
    print(number)
    # number = number.replace("-", " ")
    # number = number.split(" ")
    if "" in number:
        number.remove("")
    if " " in number:
        number.remove(" ")
    # print(number)
    final = None
    for z in number:
        z = z.strip()
        if "thous" in z:
            # print(z)
            z = z+ "and"
            x = str(text2int(z))
            if str(x) + ".wav" in thousands:
                if final is None:
                    final = thousands.get(x + ".wav")
                    # final = AudioSegment.from_wav("../Navi_bot_responses/Variables/English/Thousands/{}.wav".format(text2int(z)))
                else:
                    final += thousands.get(x + ".wav")
                    # final += AudioSegment.from_wav("../Navi_bot_responses/Variables/English/Thousands/{}.wav".format(text2int(z)))
            else:
                raise Exception("Number is missing ", x)
        elif "hundred" in z:
            x = str(text2int(z))
            if str(x) + ".wav" in hundreds:
                if final is None:
                    final = hundreds.get(x + ".wav")
                    # final = AudioSegment.from_wav("../Navi_bot_responses/Variables/English/100s English/{}.wav".format(text2int(z)))
                else:
                    final += hundreds.get(x + ".wav")
                    # final += AudioSegment.from_wav("../Navi_bot_responses/Variables/English/100s English/{}.wav".format(text2int(z)))
            else:
                raise Exception("Number is missing ", x)
        elif str(text2int(z)) + ".wav" in singles:
            x = str(text2int(z))
            if str(x) + ".wav" in singles:
                if final is None:
                    final = singles.get(x + ".wav")
                    # final = AudioSegment.from_wav(
                    #     "../Navi_bot_responses/Variables/English/Numbers 1-99/{}.wav".format(text2int(z)))
                else:
                    final += singles.get(x + ".wav")
                    # final += AudioSegment.from_wav(
                    #     "../Navi_bot_responses/Variables/English/Numbers 1-99/{}.wav".format(text2int(z)))
            else:
                raise Exception("Number is missing ", x)
        else:
            raise Exception("Number is missing ", z)
        # elif str(text2int(z)) in os.listdir("Navi_bot_responses/Variables/English/Numbers 1-99"):
        # if z == "and":
        #     continue
        # # print(os.listdir("data_splits/date_amount/units_hundreds_curated"))
        # print(z, text2int(z), number)
        # if z + ".wav" not in os.listdir("navi_new_rec/number"):
        #     if final is None:
        #         final = AudioSegment.from_wav("navi_new_rec/number/{}.wav".format(text2int(z)))
        #     else:
        #         final += AudioSegment.from_wav("navi_new_rec/number/{}.wav".format(text2int(z)))
        # else:
        #     if final is None:
        #         final = AudioSegment.from_wav("navi_new_rec/number/{}.wav".format(z))
        #     else:
        #         final += AudioSegment.from_wav("navi_new_rec/number/{}.wav".format(z))
    # if final:
    #     final.export("../formatted_numbers/{}.mp3".format(raw_number), format="mp3")
    return final



