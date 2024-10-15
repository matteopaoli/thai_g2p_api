# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import codecs
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pythainlp.tokenize import word_tokenize
from pythainlp.transliterate import romanize
from marisa_trie import Trie
import os

app = Flask(__name__)

# Initialize Flask-Limiter to limit requests based on the client's IP address
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]  # Adjust the limit as needed
)

# Load the Thai to IPA mapping data
template_file = "thai2ipa.txt"
with codecs.open(template_file, 'r', encoding='utf8') as f:
    lines = f.read().splitlines()

data = {}
for t in lines:
    data[t.split(',')[0]] = t.split(',')[1]

DEFAULT_DICT_TRIE = Trie(data.keys())

# Define the G2P function
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

# Define a route for the API with rate limiting applied
@app.route('/api/g2p', methods=['POST'])
@limiter.limit("10 per minute")  # Adjust this as needed
def g2p_api():
    # Expecting JSON data with a "text" field
    data = request.get_json()
    thai_text = data.get('text', '')
    if not thai_text:
        return jsonify({'error': 'No text provided'}), 400

    # Get the G2P result
    try:
        result = word_tokenize_to_g2p(thai_text)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
