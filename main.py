import os

import discord
import GlobalSettings
from MLibSpotify import Utilities
from MLibSpotify.SpotifyPlaylist import AuthorizationValues
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist

intents = discord.Intents.all()
# intents.messages = True
# intents.guild_messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):

    print(f'message: {message.content}')

    track_uris = GetUrisFromMessage(message.content)

    if track_uris is not None:
        print('uris found:')
        for uri in track_uris:
            print(uri)
        playlist = GetPlaylistByChannel(message.guild)
        playlist.AddTracks(tracks=track_uris)
    else:
        print('No spotify link found in message.')


def SelectPlaylist(guild):
    return '2UmDYQxgIDaKikeG53Ffd5'


def GetUrisFromMessage(message):
    track_links = Utilities.GetSpotifyLinks(message)
    if track_links is None:
        print('No links in message')
        return None
    print('links:')
    for link in track_links:
        print(link)
    return [Utilities.GetUri(link) for link in track_links]


def GetPlaylistByChannel(guild):
    authorization_values = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
                                               client_secret=GlobalSettings.CLIENT_ID)
    playlist = SpotifyPlaylist(authorization_values=authorization_values,
                               playlist_id='2UmDYQxgIDaKikeG53Ffd5')
    return playlist


client.run(GlobalSettings.TOKEN)
