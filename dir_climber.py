import os
import qbittorrentapi
import asyncio
import subprocess # because trying to use CrossSeedAutoDL as an API is suicidal
import shutil


# "Snake through" the folders (if any) of the given location and then
# run CrossSeedAutoDL for each, and use the qbittorrent API to add the torrent with
# the location set to the end location automatically. Built for situations when folders
# are sorted and hence, not cross-seedable directly.

# This is more suitable for torrents where there are few files, like movies, or archives.
# Separate edition for Music/Anime/Games/BDMVs soonTM

# configs (remember to set them before start)
input_dir = r"Q:/Movie/Remux (4k)" # set this to root dir of where you want to start looking. 
jackett_url = "http://localhost:9117" # set to url:port 
jackett_api_key = "xxxxxxxxxxxxxxxxx" # jackett api key
trackers = "tracker_a,tracker_b" # set this to a comma-separated list of trackers(no spaces)

qbittorrent_url = "http://localhost:6969" # URL of qbittorrent webui
qbittorrent_user = "admin" # username
qbittorrent_pass = "adminadmin" # password

# nuking the temp directory in case it already exists
shutil.rmtree(f"./temp")
os.mkdir(f"./temp")



# initialise the qbittorrent object with data given
qb_client = qbittorrentapi.Client(host=qbittorrent_url, username=qbittorrent_user, password=qbittorrent_pass)
print("Attempting to login to qbittorrent.")
try:
    qb_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print("Login failed. Please check config.")

print("Logged into Qbittorrent.")
print(f'Qbittorrent Version {qb_client.app_version()}.')
print(f'Qbittorrent Web API Version {qb_client.app_web_api_version()}.')

for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        try:
            # creating a directory for each file encountered.
            os.mkdir(f"./temp/{file}")
        except:
            print(f"./temp/{file} already exists.")

        command = f"python CrossSeedAutoDL.py -i \"{os.path.join(subdir)}\" -s \"./temp/{file}\" -u \"{jackett_url}\" -k \"{jackett_api_key}\" -t {trackers} --ignore-history -d 1"
        print(command)
        subprocess.run(command, shell=True) # running the command
        print(f"File Path: {os.path.join(subdir, file)}") # printing path to file
        for torrent in os.scandir(f'./temp/{file}'):
            # iterating through .torrents and adding the file to client, with respective path set
            # Prints "Ok." if the file is added fine, "Fails." if the file addition failed.
            try:
                print(qb_client.torrents_add(torrent_files=f"./temp/{file}/{torrent.name}", save_path=os.path.join(subdir), is_skip_checking=True, is_paused=True, content_layout="NoSubfolder", tags="CrossSeedAutoDL"))
            except:
                continue
