# buttonPlaya
Use my raspberry pi to play an m3u playlist and light LED when a button is pushed.

### What happened
- I installed mopidy to serve the mp3s. That makes this program a very basic mopidy client.
- I wrote this simple python program (buttonPlaya) to do actions using the mopidy post rpc api
- Button and LED programming is via hard-coded pin numbers in main.py
- Control is via playlists. Playlists are hard-coded in playa.py
- Songs on those playlists will be played.

### Starting with system
- Goal: set up buttonPlaya to start when system starts
- Done: i added 'python3 /home/pi/projects/ButtonPlaya/buttonPlaya/main.py &' to /etc/rc.local
(note the '&' starts it in a separate thread)

### To do
- Add pause functionality
- Have LED blink while playlist is being loaded

### Run before adding to rc.local
to run: start raspberry pi
then navigate to projects/ButtonPlaya/buttonPlaya
run 'python3 main.py'

### How to change music:
- use scp to connect to raspberry pi
- add files to /home/pi/mopidy/files
- update playlists in /home/pi/mopidy/playlists
- playlists are m3u files referencing tracks in /home/pi/mopidy/files
- if adding or changing a playlist name, update /home/pi/projects/ButtonPlaya/buttonPlaya/playa.py

### Notes
- mopidy has mixer
- but can change overall system volume with alsamixer
- requires gpiozero

### Links
- Mopidy POST JSON-RPC API: https://docs.mopidy.com/en/latest/api/http/

##### Mopidy setup notes:
- service config: /etc/mopidy/mopidy.conf
- i set media files dir to /home/pi/mopidy/files
- i set m3u dir to /home/pi/mopidy/playlists
- run as service: sudo systemctl start mopidy
- check status: sudo systemctl status mopidy