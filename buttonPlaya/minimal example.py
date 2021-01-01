""" This is a minimal example of using the mopidy json rpc post api to plays something on mopidy served at localhost """
import requests

payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}
r = requests.post("http://localhost:6680/mopidy/rpc", json=payload)
print(r.text)
