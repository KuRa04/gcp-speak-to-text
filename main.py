from flask import Flask, request, jsonify
from google.cloud import speech_v1p1beta1 as speech
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    # # 音声ファイルをテキスト化する
    client = speech.SpeechClient()
    file = request.files['file']
    content = file.read()
    audio = speech.RecognitionAudio(content=content)
    # audioまで確認出来た

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='ja-JP')
    response = client.recognize(config=config, audio=audio)
    transcript = ''
    print(response.results)
    for result in response.results:
        transcript += result.alternatives[0].transcript

    # # テキストを文章化する
    # # ここではダミーの文章化処理を行う
    sentences = transcript.split('。')
    text = ''
    for sentence in sentences:
        text += sentence + '\n'

    # # レスポンスとしてテキストデータを返す
    print(response)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# import os

# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     name = os.environ.get("NAME", "World")
#     return "Hello {}!".format(name)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))