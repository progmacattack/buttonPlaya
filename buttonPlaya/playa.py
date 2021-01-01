import requests
import json
from time import sleep

class PlaylistPosition:
    def __init__(self, playlist, track, timePosition):
        self.track = track
        self.timePosition = timePosition
        self.playlist = playlist

class Playa:
    def __init__(self):
        self.mopidyUrl = "http://localhost:6680/mopidy/rpc"
        self.playlistPositions = {}

    """ Get m3u playlists """
    def __getPlaylists(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playlists.as_list"}
        r = requests.post(self.mopidyUrl, json=payload)

    """ returns an array of uris playable by mopidy """
    def __getTrackUrisFromPlaylist(self, m3uName):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playlists.get_items", "params":{"uri": "m3u:" + m3uName}}
        r = requests.post(self.mopidyUrl, json=payload)
        response = json.loads(r.text)['result']
        urisFromPlaylist = []
        for result in response:
            if[result['type'] == "track"]:
                urisFromPlaylist.append(result['uri'])
        return urisFromPlaylist

    def __loadTracks(self, uris):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.add", "params":{"uris": uris}}
        requests.post(self.mopidyUrl, json=payload)

    def __play(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.play"}
        requests.post(self.mopidyUrl, json=payload)

    def __stop(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.stop"}
        requests.post(self.mopidyUrl, json=payload)

    def __pause(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.pause"}
        requests.post(self.mopidyUrl, json=payload)

    def __setRepeat(self, doRepeat):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.set_repeat", "params":{"value": doRepeat}}
        requests.post(self.mopidyUrl, json=payload)

    """ Clears tracks. """
    def __clearTracks(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.tracklist.clear"}
        requests.post(self.mopidyUrl, json=payload)

    """ Get currently playing track as mopidy tl track """
    def __getCurrentTrack(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_current_tl_track"}
        r = requests.post(self.mopidyUrl, json=payload)
        return json.loads(r.text)['result']['track']

    """ Get current time position within track in milliseconds """
    def __getCurrentTimePosition(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_time_position"}
        r = requests.post(self.mopidyUrl, json=payload)
        return json.loads(r.text)['result']

    """ Set level volume between 0 and 100 """
    def __setVolume(self, level):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.mixer.set_volume", "params":{"volume": level}}
        requests.post(self.mopidyUrl, json=payload)

    """ Load the provided tl track model """
    def __setTrack(self, playPosition):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.play", "params":{"tl_track": playPosition.track}}
        requests.post(self.mopidyUrl, json=payload)

    """ Set the current track to the provided position in milliseconds """
    def __setTrackPosition(self, playPosition):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.seek", "params":{"time_position": playPosition.timePosition}}
        requests.post(self.mopidyUrl, json=payload)

    """ Pass name of playlist located in /home/pi/mopidy/playlists. For example, "bach.m3u" """
    def playPlaylist(self, m3uName):
        urisFromPlaylist = self.__getTrackUrisFromPlaylist(m3uName)
        self.__clearTracks()
        self.__loadTracks(urisFromPlaylist)
        self.__setRepeat(True)
        self.__setVolume(100)
        self.__play()

    """ Pause a playlist, saving state for later continuation """
    def pausePlaylist(self, m3uName):
        self.__pause()
        track = self.__getCurrentTrack()
        print("Current track is: " + json.dumps(track))
        timePosition = self.__getCurrentTimePosition()
        print("Current time is: " + str(timePosition))
        playlistPosition = PlaylistPosition(m3uName, track, timePosition)
        self.playlistPositions[m3uName] = playlistPosition
        self.__pause()

    """ Continue a playlist from the last known track and position """
    def continuePlaylist(self, m3uName):
        playlistPosition = self.playlistPositions[m3uName]
        self.__setVolume(0)
        self.playPlaylist(m3uName)
        self.__setTrack(playlistPosition)
        sleep(0.1)
        self.__setTrackPosition(playlistPosition)
        self.__setVolume(100)
        self.__play()
        
    def canContinuePlaylist(self, m3uName):
        if m3uName in self.playlistPositions:
            print(m3uName + " is in the playlist position dictionary")
            return True
        else:
            return False



    def stop(self):
        self.__stop()


