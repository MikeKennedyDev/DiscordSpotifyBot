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

    track_uris = GetIdsFromMessage(message.content)

    if track_uris is not None:
        print('uris found:')
        for uri in track_uris:
            print(uri)
        playlist = GetPlaylistByChannel(message.guild)
        print('Trying to add tracks')
        playlist.AddTracks(tracks=track_uris)
    else:
        print('No spotify link found in message.')


def SelectPlaylist(guild):
    return '2UmDYQxgIDaKikeG53Ffd5'


def GetIdsFromMessage(message):
    track_links = Utilities.GetSpotifyLinks(message)
    if track_links is None:
        print('No links in message')
        return None
    print('links:')
    for link in track_links:
        print(link)
    return [Utilities.GetTrackId(link) for link in track_links]


def GetPlaylistByChannel(guild):
    authorization_values = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
                                               client_secret=GlobalSettings.CLIENT_SECRET,
                                               scope='playlist-read-collaborative playlist-modify-public')

    playlist = SpotifyPlaylist(authorization_values=authorization_values,
                               playlist_id='2UmDYQxgIDaKikeG53Ffd5')
    print('Completed playlist modeling')
    return playlist


client.run(GlobalSettings.TOKEN)

# print('Playlist test')
# TestPlaylistId = '2UmDYQxgIDaKikeG53Ffd5'
# TestTrackIds = ['56rgqDNRIqKq0qIMdu7r4r', '1rWzYSHyZ5BiI4DnDRCwy7']
# auth = AuthorizationValues(client_id=GlobalSettings.CLIENT_ID,
#                            client_secret=GlobalSettings.CLIENT_SECRET,
#                            scope='playlist-read-collaborative playlist-modify-public')
# playlist = SpotifyPlaylist(auth, playlist_id=TestPlaylistId)
#
# original_num_tracks = len(playlist.GetAllTracks())
# print(f'Originally {original_num_tracks} tracks')
#
# playlist.AddTracks(TestTrackIds)
# print(f'{len(TestTrackIds)} tracks added')
#
# new_num_tracks = len(playlist.GetAllTracks(force_refresh=True))
# print(f'Now {new_num_tracks} tracks')
# print('Playlist test complete')
