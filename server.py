from flask import Flask
from flask import render_template, request, jsonify
import string
import json
import requests



app = Flask(__name__)

invalidChars = set(string.punctuation)

def searchPrefixES(prefix):

    query = json.dumps({"countries": {"prefix": prefix, "completion": {"field": "name_suggest"}}})
    r = requests.post('http://localhost:9200/countries/_suggest?pretty', query)
    dump = r.json()
    data = dump['countries'][0]
    items = []
    for d in data['options']:  # First Example
        items.append(d['_source']['name_suggest']['input'])
    return items


@app.route('/')
def home():
    html = render_template('home.html', name="IAPR AutoComplete Demo")
    return html


@app.route('/searchPrefix')
def searchPrefix():
    query = request.args.get('query')
    prefix = query.split(" ")[-1]
    print(query)
    print(prefix)
    top10 = searchPrefixES(prefix)
    return jsonify({"prediction": top10})


if __name__ == '__main__':
    app.run()
