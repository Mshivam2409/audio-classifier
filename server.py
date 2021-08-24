import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from inference.audio import AudioClassifier
from flask import Flask, request

app = Flask(__name__)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["audio"]
        top = int(request.form["top"])
        result = AudioClassifier.predict(f, top)
        return {"result": result}


if __name__ == "__main__":
    print(AudioClassifier.model.summary())
    app.run("0.0.0.0", 6000)
