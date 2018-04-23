from flask import Flask
from flask import request
from flask import jsonify

import numpy
from word_loader import WordLoader

app = Flask(__name__)

word_loader = WordLoader()

@app.route("/api/words", methods=["GET"])
def hello():
    language = request.args["language"]
    real_words = int(request.args["realWords"])
    fake_words = int(request.args["fakeWords"])

    return jsonify({
        'realWords': [x.serialize() for x in get_real_words(language, real_words)],
        'fakeWords': [x.serialize() for x in get_fake_words(language, fake_words)]
    })

def get_real_words(language, real_words):
    words = word_loader.get_real_words_for(language=language)

    return list(numpy.random.choice(words, size=real_words, replace=False))

def get_fake_words(language, fake_words):
    words = word_loader.get_fake_words_for(language=language)

    return list(numpy.random.choice(words, size=fake_words, replace=False))

if __name__ == "__main__":
    app.run()