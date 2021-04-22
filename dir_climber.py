import qbittorrent-api
import asyncio
import subprocess # because trying to user CrossSeedAutoDL as an API is suicidal
import shutil


# Aim will be to "snake through" the folders (if any) of the given location and then
# run cross-seed-autoDL for each, and use the qbittorrent API to add the torrent with
# the location set to the end location automatically. Currently does 1 layer depth.

# configs (remember to set them before start)
input_dir = "/data" # set this to root dir of where you want to start looking. 
create_subfolder = False # set this to True in case you have torrents that are in the proper folder -> file format and not as individual files.
save_path = "./torrents" # this is just to move your torrents elsewhere in case you need them later on.
jackett_url = "http://localhost:6969" # set to url:port 
jackett_api_key = "abcdef12345" # jackett api key
trackers = ["abc","xyz"] # set this to a dict of trackers you need

qbittorrent_url = "http://localhost:6969" # URL of qbittorrent webui
qbittorrent_user = "admin" # username
qbittorrent_pass = "adminadmin" # password


