import os

import discord
import requests
from MLibSpotify import Utilities
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
# TODO: Do I need all intents?

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):
    track_ids = GetIdsFromMessage(message.content)

    # message.guild = Server name
    # message.channel = name of channel in server

    if track_ids is not None:
        playlist_id = GetPlaylistIdByChannel(message.guild)
        for track_id in track_ids:
            print(f'Adding track:{track_id} to playlist:{playlist_id}')
            response = requests.get(f'{os.getenv("API_BASE")}/addTrack/{playlist_id}/{track_id}')
            if response.ok:
                print('Track added')
            else:
                None
                # TODO: Throw if response if bad
    else:
        print('No spotify link found in message.')


def GetIdsFromMessage(message):
    track_links = Utilities.GetSpotifyLinks(message)
    if track_links is None:
        print('No links in message')
        return None
    print('links:')
    for link in track_links:
        print(link)
    return [Utilities.GetTrackId(link) for link in track_links]


def GetPlaylistIdByChannel(guild):
    # print(guild)
    return '2UmDYQxgIDaKikeG53Ffd5'


client.run(os.getenv("TOKEN"))
