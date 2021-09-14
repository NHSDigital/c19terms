import os
import json

__version__ = '0.0.0'


def get_terms():
    terms_path = os.path.join(os.path.dirname(__file__), 'terms.json')
    with open(terms_path, 'r') as f:
        return json.loads(f.read())
