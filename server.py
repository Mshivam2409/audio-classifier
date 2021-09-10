import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from inference.audio import AudioClassifier
from flask import Flask, request
import requests
import socketio

sio = socketio.Client()
sio.connect("http://localhost:4000")


app = Flask(__name__)


@app.route("/check", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["audio"]
        token = request.form["auth"]
        qid = request.form["qid"]
        answer = requests.get(
            "http://localhost:5000/answer_full/{}".format(qid)
        ).json()["answer"]
        result = AudioClassifier.predict(f, answer)
        f.seek(0)
        files = {"file": f.read()}
        requests.post(
            files=files,
            data={
                "recType": "answer",
                "correct": result,
                "expectedAnswer": answer,
                "transcript": "",
            },
        )
        sio.emit("audioanswer", data={"auth": token, "correct": result})
        return {"result": result}


if __name__ == "__main__":
    app.run("0.0.0.0", 6000)
