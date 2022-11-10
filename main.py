import os
import threading

import discord
from MLibSpotify import Links
from MLibSpotify.SpotifyPlaylist import SpotifyPlaylist
from dotenv import load_dotenv
import pyodbc

load_dotenv()
__playlist_cache = []

sql_connection = pyodbc.connect('DRIVER=' + os.environ["DRIVER"] +
                                ';SERVER=tcp:' + os.environ["SERVER"] +
                                ';PORT=1433;DATABASE=' + os.environ["DATABASE"] +
                                ';UID=' + os.environ["UNAME"] +
                                ';PWD=' + os.environ["PASSWORD"])

cursor = sql_connection.cursor()

intents = discord.Intents.all()
# TODO: Do I need all intents?

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in: {client.user}')


@client.event
async def on_message(message):
    try:

        # Ignore self messages
        if 'PlaylistMaintainer' in str(message.author):
            return

        if message.content == '/help':
            await message.channel.send(GetHelpMessage(message))
            return

        elif '/AddPlaylist' in message.content:
            result = MapNewPlaylist(message)
            await message.channel.send(result)
            return

        elif '/RemovePlaylist' in message.content:
            RemoveMappedPlaylist(message)
            await message.channel.send("Playlist unlinked from current channel")
            return

        elif GetIdsFromMessage(message.content) is not None:

            track_ids = GetIdsFromMessage(message.content)
            playlists = GetPlaylistsByChannel(message)

            for playlist in playlists:
                try:
                    playlist.AddTracks(track_ids)
                except:
                    await message.channel.send(f"Song already exists in {playlist.PlaylistName}")

        else:
            print('No spotify link found in message.')

    except:
        await message.channel.send(f"Oh boy something went wrong, you shouldn't see this. Shutting down.")
        exit()


def GetIdsFromMessage(message):
    try:
        track_links = Links.GetSpotifyLinks(message)

        if track_links is None:
            return None

        return [Links.GetTrackId(link) for link in track_links]

    except:
        return None


def GetPlaylistsByChannel(message):
    cursor.execute('''
    SELECT PlaylistId FROM [dbo].[Playlists]
    WHERE DiscordServer = ?
    AND DiscordChannel = ?
        ''', [str(message.guild), str(message.channel)])

    ids = cursor.fetchall()
    playlists = []

    if ids is not None:
        playlist_ids = [id[0] for id in ids]

        for playlist_id in playlist_ids:
            print(f'Using playlist id: {playlist_id}')

            # check __playlist cache before calling spotify API
            if __playlist_cache is not None and playlist_id in [playlist.PlaylistId for playlist in __playlist_cache]:
                print('Playlist found in playlist cache.')
                playlists.append(next(p for p in __playlist_cache if p.PlaylistId == playlist_id))

            else:
                print('Playlist not found in playlist cache, generating new playlist object.')
                playlist = SpotifyPlaylist(playlist_id=playlist_id,
                                           client_id=os.environ["CLIENT_ID"],
                                           client_secret=os.environ["CLIENT_SECRET"],
                                           refresh_token=os.environ["REFRESH_TOKEN"])
                playlists.append(playlist)
                __playlist_cache.append(playlist)

        return playlists


def MapNewPlaylist(message):
    try:
        playlist_url = message.content.split()[1]
        playlist_id = Links.GetPlaylistId(playlist_url)
        print(f'Mapping playlist: {playlist_id} to current channel')

        cursor.execute('''
        INSERT INTO [dbo].[Playlists]
        VALUES (?, ?, ?);
        ''', [playlist_id, str(message.guild), str(message.channel)])

        sql_connection.commit()
        return "Playlist linked to current channel."

    except pyodbc.IntegrityError as e:
        if e.args[0] == '23000':
            return "Playlist already mapped to current channel."
        else:
            return "Error mapping playlist. Please try again."

    except:
        return "Error mapping playlist. Please try again."


def RemoveMappedPlaylist(message):
    playlist_url = message.content.split()[1]
    playlist_id = Links.GetPlaylistId(playlist_url)
    print(f'Mapping playlist: {playlist_id} to current channel')

    cursor.execute('''
DELETE FROM [dbo].[Playlists]
WHERE PlaylistId = ?
    AND DiscordServer = ?
    AND DiscordChannel = ?
    ''', [playlist_id, str(message.guild), str(message.channel)])

    sql_connection.commit()


def GetHelpMessage(message):
    currentPlaylists = GetPlaylistsByChannel(message)
    displayPlaylists = '\n'.join([f"{playlist.PlaylistName} ({playlist.PlaylistUrl})" for playlist in currentPlaylists])

    return f'''
The playlist(s) currently mapped to this channel are:
{displayPlaylists}

Simply post a spotify track in the channel to add it to the playlist(s).

To map a playlist to this channel, use the command:
/AddPlaylist <playlist-url>

To disconnect a playlist from this channel, use the command:
/RemovePlaylist <playlist-url>

'''


def FlushPlaylistCache():
    print('Flushing playlist cache')
    __playlist_cache = []
    threading.Timer(86400, FlushPlaylistCache).start()


if __name__ == '__main__':
    print('starting up')

    # Flush playlist cache daily
    FlushPlaylistCache()

    client.run(os.environ["TOKEN"])
