import io
import time

from fastapi import FastAPI, Response, requests

from final_automatic_tts_generator.automatic_tts_generate import generate_tts_files

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#
@app.post("/wav")
def streamwav():
    def generate(template_name=None, message=None):

        data = generate_tts_files(
            message=message,
            utterance_name=template_name)
        buf = io.BytesIO()
        data.export(buf)
        return buf.getvalue()
    start_time = time.time()
    data = requests.Request.json()
    print(data)
    audio = generate(message=data.get("message"), template_name=data.get("template_name"))
    print(time.time() - start_time)
    return Response(audio,
                    mimetype="audio/wav")
#
