import os

import discord
import requests
from MLibSpotify import Links, Utilities
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
# TODO: Do I need all intents?

client = discord.Client(intents=intents)
__help_message = '''
The playlist currently mapped to this channel is: XXX
Simply post a spotify track in the channel to add it to the playlist.
To map a playlist to this channel, use the command:
/AddPlaylist <playlist-url>
'''


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):
    if message.content == '/help':
        await message.channel.send(__help_message)
        return

    if '/AddPlaylist' in message.content:
        await message.channel.send('Oh we finna add this bitch')
        MapNewPlaylist(message)
        return

    track_ids = GetIdsFromMessage(message.content)

    # message.guild = Server name
    # message.channel = name of channel in server

    if track_ids is not None:
        playlist_id = GetPlaylistIdByChannel(message.guild)
        for track_id in track_ids:
            print(f'Adding track:{track_id} to playlist:{playlist_id}')
            response = requests.post(f'{os.environ["API_BASE"]}/addTrack/{playlist_id}/{track_id}')
            if response.ok:
                print('Track added')
            else:
                error_msg = response.json()['error']['message']
                print(f"Track add failure: "
                      f"response: {response}"
                      f"error message: {error_msg}")
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


def GetPlaylistIdByChannel(guild):
    # print(guild)
    return '2UmDYQxgIDaKikeG53Ffd5'


def MapNewPlaylist(message):
    playlist_url = message.content.split()[1]
    print(f'Adding playlist: {playlist_url}')

    playlist_id = Links.GetPlaylistId(playlist_url)
    print(f'playlist_id: {playlist_id}')

    return None


client.run(os.environ["TOKEN"])
