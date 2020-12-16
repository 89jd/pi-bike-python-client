import json
from types import SimpleNamespace

with open('client.json') as f:
    properties = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
