import discord
import GlobalSettings
from MLibSpotify import Utilities
from MLibSpotify.SpotifyPlaylist import AuthorizationValues
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist

intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):
    links = Utilities.GetSpotifyLinks(message.content)
    if links is not None:
        playlist_id = SelectPlaylist(message.guild)
        authorization_values = AuthorizationValues(client_id='',
                                                   client_secret='')
        SpotifyPlaylist(authorization_values=authorization_values,
                        playlist_id=playlist_id)

    print(message.guild)


def SelectPlaylist(guild):
    return '2UmDYQxgIDaKikeG53Ffd5'


client.run(GlobalSettings.TOKEN)
