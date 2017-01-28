from flask import Flask
from flask import render_template, request, jsonify
import string
import json
import requests

app = Flask(__name__)
invalidChars = set(string.punctuation)

def searchPrefixES(prefix):

    #1. Construct json query
    #2. POST query to the server
    #3. Process the response
    #4. Return a list of suggestions

@app.route('/')
def home():
    html = render_template('home.html', name="IAPR AutoComplete Demo")
    return html

@app.route('/searchPrefix')
def searchPrefix():
    query = request.args.get('query')
    prefix = query.split(" ")[-1]
    top10 = searchPrefixES(prefix)
    return jsonify({"prediction": top10})

if __name__ == '__main__':
    app.run()

