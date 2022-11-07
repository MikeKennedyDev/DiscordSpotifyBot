import os

import discord
import requests
import pyodbc
from MLibSpotify import Links
from dotenv import load_dotenv

load_dotenv()

import pyodbc

sql_connection = pyodbc.connect('DRIVER=' + os.getenv("DRIVER") +
                                ';SERVER=tcp:' + os.getenv("SERVER") +
                                ';PORT=1433;DATABASE=' + os.getenv("DATABASE") +
                                ';UID=' + os.getenv("UNAME") +
                                ';PWD=' + os.getenv("PASSWORD"))
cursor = sql_connection.cursor()

intents = discord.Intents.all()
# TODO: Do I need all intents?

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):
    if message.content == '/help':
        await message.channel.send(GetHelpMessage())
        return

    if '/AddPlaylist' in message.content:
        MapNewPlaylist(message)
        return

    track_ids = GetIdsFromMessage(message.content)

    if track_ids is not None:
        playlist_id = GetPlaylistIdByChannel(message)
        print(f'Playlist_id found: {playlist_id}')
        for track_id in track_ids:
            print(f'Adding track: {track_id} to playlist: {playlist_id}')
            response = requests.post(f'{os.environ["API_BASE"]}/addTrack/{playlist_id}/{track_id}')
            if response.ok:
                print('Track added')
            else:
                print(response.json())
                return
                # error_msg = response.json()['error']['message']
                # print(f"Track add failure: "
                #       f"response: {response}"
                #       f"error message: {error_msg}")
    else:
        print('No spotify link found in message.')


def GetIdsFromMessage(message):

    track_links = Links.GetSpotifyLinks(message)
    if track_links is None:
        print('No links in message')
        return None
    print('links:')
    for link in track_links:
        print(link)
    return [Links.GetTrackId(link) for link in track_links]


def GetPlaylistIdByChannel(message):
    cursor.execute('''
    SELECT PlaylistId FROM [dbo].[Playlists]
    WHERE DiscordServer = ?
    AND DiscordChannel = ?
        ''', [str(message.guild), str(message.channel)])

    playlist_id = cursor.fetchone()
    if not playlist_id:
        raise Exception("No playlist currently associated with this channel")

    return playlist_id[0]


def MapNewPlaylist(message):
    playlist_url = message.content.split()[1]
    print(f'Mapping playlist: {playlist_url} to current channel')

    # message.guild = Server name
    # message.channel = name of channel in server
    print(f'Server: {message.guild}')
    print(f'Channel: {message.channel}')

    cursor.execute('''
SELECT * FROM [dbo].[Playlists]
WHERE DiscordServer = ?
AND DiscordChannel = ?
    ''', [str(message.guild), str(message.channel)])


    while 1:
        row = cursor.fetchone()
        if not row:
            print('Playlist not currently mapped')
            break
        print(row)

    playlist_id = Links.GetPlaylistId(playlist_url)
    print(f'playlist_id: {playlist_id}')

    return None


def GetHelpMessage():
    return f'''
The playlist currently mapped to this channel is: {"poop"}
Simply post a spotify track in the channel to add it to the playlist.
To map a playlist to this channel, use the command:
/AddPlaylist <playlist-url>
'''


if __name__ == '__main__':
    print('starting up')
    client.run(os.environ["TOKEN"])
