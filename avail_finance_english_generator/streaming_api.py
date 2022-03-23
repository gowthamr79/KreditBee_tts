import time

from flask import Flask, Response, request
import io

from automatic_tts_generate import generate_tts_files

app = Flask(__name__)


@app.route("/wav", methods=["POST"])
def streamwav():
    def generate(template_name=None, message=None):

        data = generate_tts_files(
            message=message,
            utterance_name=template_name)
        buf = io.BytesIO()
        data.export(buf, bitrate="32k")
        return buf.getvalue()
    start_time = time.time()
    data = request.json
    print(data)
    audio = generate(message=data.get("message"), template_name=data.get("template_name"))
    print(time.time() - start_time)
    return Response(audio,
                    mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True, port=7000)