import os
import json


def get_terms():
    terms_path = os.path.join(os.path.dirname(__file__), 'terms.json')
    with open(terms_path, 'r') as f:
        return json.loads(f.read())
