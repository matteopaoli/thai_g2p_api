from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import romanize
from marisa_trie import Trie
import codecs
from os import path

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = path.dirname(path.abspath(__file__))
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)

template_file = path.join(BASE_DIR, "thai2ipa.txt")
with codecs.open(template_file, 'r', encoding='utf8') as f:
    lines = f.read().splitlines()

data = {}
for t in lines:
    data[t.split(',')[0]] = t.split(',')[1]

DEFAULT_DICT_TRIE = Trie(data.keys())

def word_tokenize_to_g2p(text):
    wordall = word_tokenize(text, custom_dict=DEFAULT_DICT_TRIE, engine="newmm")
    result = []
    for a in wordall:
        try:
            result.append(data[a])
        except KeyError:
            word_list_icu = word_tokenize(a, engine="icu")
            for b in word_list_icu:
                result.append(romanize(b, engine='pyicu'))
    return '|'.join(result)

@app.route('/api/g2p', methods=['POST'])
@limiter.limit("10 per minute")
def g2p_api():
    data = request.get_json()
    thai_text = data.get('text', '')
    if not thai_text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        result = word_tokenize_to_g2p(thai_text)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
