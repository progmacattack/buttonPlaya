import requests
import json

class Playa:
    def __init__(self):
        self.mopidyUrl = "http://localhost:6680/mopidy/rpc"

    """ Get m3u playlists """
    def __getPlaylists(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playlists.as_list"}
        r = requests.post(self.mopidyUrl, json=payload)

    """ returns an array of uris playable by mopidy """
    def __getTrackUrisFromPlaylist(self, m3uName):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playlists.get_items", "params":{"uri": "m3u:" + m3uName}}
        r = requests.post(self.mopidyUrl, json=payload)
        print(r.text)
        response = json.loads(r.text)['result']
        urisFromPlaylist = []
        for result in response:
            if[result['type'] == "track"]:
                urisFromPlaylist.append(result['uri'])
        return urisFromPlaylist

    def __loadTracks(self, uris):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params":{"uris": uris}}
        r = requests.post(self.mopidyUrl, json=payload)

    def __play(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}
        r = requests.post(self.mopidyUrl, json=payload)

    def __stop(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}
        r = requests.post(self.mopidyUrl, json=payload)

    def __setRepeat(self, doRepeat):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.set_repeat", "params":{"value": doRepeat}}
        requests.post(self.mopidyUrl, json=payload)

    """ Clears tracks. """
    def __clearTracks(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear"}
        requests.post(self.mopidyUrl, json=payload)

    """ Set level volume between 0 and 100 """
    def __setVolume(self, level):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.mixer.set_volume", "params":{"volume": level}}
        requests.post(self.mopidyUrl, json=payload)

    """ Pass name of playlist located in /home/pi/mopidy/playlists. For example, "bach.m3u" """
    def playPlaylist(self, m3uName):
        urisFromPlaylist = self.__getTrackUrisFromPlaylist(m3uName)
        self.__clearTracks()
        self.__loadTracks(urisFromPlaylist)
        self.__setRepeat(True)
        self.__setVolume(100)
        self.__play()

    def stop(self):
        self.__stop()


