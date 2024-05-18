# Scripts for use with CC: Tweaked
These scripts were made for our personal server, so setup might differ than shown here.

## Music Player
Uses a flask server to download and encode audio from youtube videos for use with the CC speaker. Does not work perfectly but its pretty good most of the time! 

### Current best setup
1. Run `youtube_server.py`. This server needs to be running for the youtube links to function.
   - Note: If the server is on your network, you need to change the CC config for the lua scripts to work. If it is not on your network, you need to port forward.
3. Create a computer with a modem on top and a speaker connected. Add the controller script using pastebin ([Link here](https://pastebin.com/viupKAm0).
4. Make more computers wherever you want the music to play, and connect as many speakers as you want to these computers with wired modems.
5. Since synchronization is tricky, if you want speakers that are near eachother to play in sync you should use the wired speaker controller. Put the wired speaker controller script on these listening computers ([Pastebin here](https://pastebin.com/gE15Th5J)).
6. Run the listener script on the listening computers.
7. Run the controller script with the arguments `play (link)` with link being some youtube link. Should start playing!
