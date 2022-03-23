import hashlib
from re import template
import time

from flask import Flask, Response, request, send_file, make_response
import io

import avail_finance_english_generator.automatic_tts_generate as eatg
import avail_finance_hindi_generator.automatic_tts_generate_hindi as hatgh
import avail_finance_kannada_tts_generator.automatic_tts_generate_kannada as katgk



app = Flask(__name__)
@app.route("/wav", methods=["GET"])
def streamwav():
    def generate(template_name=None, message=None, language=None):
        print(language)
        if language.lower() == "english":
            data = eatg.classify_static_dynamic_template(message, template_name)
        elif language.lower() == "hindi":
            data = hatgh.classify_static_dynamic_template(message, template_name)
        # elif language.lower() == "tamil":
        #     data = tatgh.classify_static_dynamic_template(message, template_name)
        # elif language.lower() == "telugu":
        #     data = teatgh.classify_static_dynamic_template(message, template_name)
        # elif language.lower() == "bengali":
        #     data = beath.classify_static_dynamic_template(message,template_name)
        elif language.lower() == "kannada":
            data = katgk.classify_static_dynamic_template(message,template_name)
        # elif language.lower() == "malayalam":
        #     data = meath.classify_static_dynamic_template(message,template_name)
        # elif language.lower() == "punjabi":
        #     data = peath.classify_static_dynamic_template(message,template_name)
        # elif language.lower() == "marathi":
        #     data = mara.classify_static_dynamic_template(message,template_name)
       # data = generate_tts_files(
        #     message=message,
        #     utterance_name=template_name)
        buf = io.BytesIO()
        data.export(buf, bitrate="128k", format="wav")
        return buf.getvalue()

    start_time = time.time()
    message = request.args.get("message")
    hash_object = hashlib.md5(message.encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    template_name = request.args.get("template_name")
    language = request.args.get("language")
    # print(data)
    audio = generate(message=message, template_name=template_name,
                     language=language)
    print(time.time() - start_time)
    response = make_response(audio)
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename={}.wav'.format(file_name)
    return response
    # return send_file(audio,
    #                  mimetype="audio/wav",
    #                  as_attachment=True,
    #                  attachment_filename="test.wav")


if __name__ == "__main__":
    # app.run(debug=True, port=7000)
    app.run(host="127.0.0.1",port=7004,threaded=True)
